import os
import json

import torch
from PIL import Image
from torchvision import transforms
import matplotlib.pyplot as plt
import glob

from model_v3 import mobilenet_v3_large
from openpyxl import Workbook


def main():
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    data_transform = transforms.Compose(
        [transforms.Resize(256),
         transforms.CenterCrop(224),
         transforms.ToTensor(),
         transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])

    # load image
    accuracy = []
    name = []
    img_path = r".\mobilenetv3\val_cal"
    assert os.path.exists(img_path), "file: '{}' dose not exist.".format(img_path)
    # create model
    model = mobilenet_v3_large(num_classes=54).to(device)
    # load model weights
    model_weight_path = "./MobileNetV3_large.pth"
    model.load_state_dict(torch.load(model_weight_path, map_location=device))
    model.eval()
    for e in glob.glob(img_path + '/*'):
        print(e.split("\\")[-1])
        name.append(e.split("\\")[-1])
        accuracy1 = []
        a = 0
    #for i in range(10):
        for i in glob.glob(e+'/*.jpg'):
            a += 1
            img = Image.open(i)
            plt.imshow(img)
            # [N, C, H, W]
            img = data_transform(img)
            # expand batch dimension
            img = torch.unsqueeze(img, dim=0)

            # read class_indict
            json_path = './class_indices.json'
            assert os.path.exists(json_path), "file: '{}' dose not exist.".format(json_path)

            with open(json_path, "r") as f:
                class_indict = json.load(f)
            with torch.no_grad():
                # predict class
                output = torch.squeeze(model(img.to(device))).cpu()
                predict = torch.softmax(output, dim=0)
                predict_cla = torch.argmax(predict).numpy()

            print_res = "class: {}   prob: {:.3}".format(class_indict[str(predict_cla)],
                                                         predict[predict_cla].numpy())
            print(print_res)
            # plt.title(print_res)
            # for i in range(len(predict)):
            #     print("class: {:10}   prob: {:.3}".format(class_indict[str(i)],
            #                                               predict[i].numpy()))
            plt.show()
            if class_indict[str(predict_cla)] == e.split("\\")[-1]:
                accuracy1.append(1.0)
            else:
                accuracy1.append(0.0)
        print(sum(accuracy1) / a)
        accuracy.append(sum(accuracy1) / a)
    dict_all = dict(zip(name, accuracy))
    print(dict_all)
    wb = Workbook()
    ws = wb.active
    ws.append(['name', 'accuracy'])
    for key in dict_all:
        print(key, dict_all[key])
        ws.append([key, dict_all[key]])
    wb.save(r'.\mobile_V3_large_data.xlsx')



if __name__ == '__main__':
    main()
