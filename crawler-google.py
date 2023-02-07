# -*- coding: utf-8 -*-
'''
The purpose of this code is to simulate human behavior and save the image URL of Google images, and finally save it in npy format.
'''


import os
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from pyquery import PyQuery as pq
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import win32api
import win32con
import numpy as np
import re





# Define a taobao class
class taobao_infos:

    def __init__(self):
        options = webdriver.ChromeOptions()
        #options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2}) 
        options.add_experimental_option('excludeSwitches',
                                        ['enable-automation'],)  # This step is very important. It is set to developer mode to prevent Selenium from being recognized by major websites
        #options.add_argument("--headless")

        self.browser = webdriver.Chrome(executable_path=chromedriver_path, options=options)
        #self.browser1 = webdriver.Chrome(executable_path=chromedriver_path, options=options)
        self.browser.implicitly_wait(5)
        self.wait = WebDriverWait(self.browser, 20)
    # Simulate sliding down
    def swipe_down(self, second):
        for i in range(int(second / 0.1)):
            js = "var q=document.documentElement.scrollTop=" + str(300 + 200 * i)
            self.browser.execute_script(js)
            sleep(0.1)
        js = "var q=document.documentElement.scrollTop=100000"
        self.browser.execute_script(js)
        sleep(0.2)

    def swipe_up(self):
        js = "var q=document.documentElement.scrollTop=0"
        self.browser.execute_script(js)
        sleep(0.2)

    def crawl_good_data(self,url_name):

        if os.path.exists(url_name) ==False:
            os.makedirs(url_name)
        self.browser.get(url_data.get(url_name))

        # The essence is to simulate the manual downward browsing of goods, that is, to simulate the sliding operation to prevent being recognized as a robot
        # self.swipe_down(30)
        html = self.browser.page_source

        # Pq module parses web page source code
        doc = pq(html)

        name = self.browser.find_elements(By.XPATH,'// *[ @ id = "i7"] / div[1] / span / span / div/ a / span')
        iiiiii = 'i7'
        if len(name) == 0:
            name = self.browser.find_elements(By.XPATH, '// *[ @ id = "i8"] / div[1] / span / span / div/ a')
            iiiiii='i8'
        print(iiiiii)
        print('lenname:',len(name))
        ccc = 0
        ddd = 0
        fff = 0
        img_list= []
        for name_i in name:
            fff +=1
            ccc += 1
            sleep(2)
            if ccc >= 2:
                try:
                    but1 = self.browser.find_element(By.XPATH,'// *[ @ id = "{}"] / div[1] / span / span / div[{}]/ a / span'.format(iiiiii,ccc))
                    #print(but1)
                except:
                    print("没找到这个xpath，继续下一个")
                    continue
                print(but1)
                try:
                    but1.click()
                except:
                    sleep(1)
                    #// *[ @ id = "i7"] / div[3] / div
                    self.browser.find_element(By.XPATH, '// *[ @ id = "{}"] / div[3] / div'.format(iiiiii)).click()
                    sleep(1)
                    but1.click()
            else:
                name_i.click()
            sleep(2)
            self.swipe_down(20)
            try:
                button1 = self.browser.find_element(By.XPATH,'// *[ @ id = "islmp"] / div / div / div / div[2] / span')
                button1.click()
            except:
                pass
            sleep(1)
            self.swipe_down(20)

            try:     #//*[@id="islmp"]/div/div/div/div/div[1]/div[2]/div[2]/input
                button = self.browser.find_element(By.XPATH,'//*[@id="islmp"]/div/div/div/div/div[1]/div[2]/div[2]/input')
                button.click()
            except:
                pass
            self.swipe_down(20)
            try:     #//*[@id="islmp"]/div/div/div/div/div[1]/div[2]/div[2]/input
                button = self.browser.find_element(By.XPATH,'// *[ @ id = "islmp"] / div / div / div / div[1] / div[2] / div[2] / input')
                button.click()
            except:
                pass
            sleep(3)
            self.swipe_down(50) #50
            bbb = 0
            name_11 = self.browser.find_elements(By.XPATH,'//*[@id="islrg"]/div[1]/div/a[1]/div[1]/img')
            print(len(name_11))
            for name_11_i in name_11:
                if bbb<=len(name_11)-6:   #len(name_11)-6
                    bbb += 1
                    ddd += 1
                    if bbb % 25 == 0:
                        continue
                    previewImageXPath = """//*[@id="islrg"]/div[1]/div[%s]/a[1]/div[1]/img""" % (bbb)

                    try:
                        previewImageElement = self.browser.find_element(By.XPATH, previewImageXPath)
                        previewImageURL = previewImageElement.get_attribute("src")

                    except:
                        print('没有小图片，下一个')
                        continue

                    try:
                        name_11_i.click()
                        print("正常打开")
                        timeStarted = time.time()

                        while True:
                            try:
                                imageURL = self.browser.find_element(By.XPATH,'//*[@id="Sva75c"]/div/div/div[2]/div[2]/div[2]/c-wiz/div[2]/div[1]/div[1]/div[2]/div/a/img').get_attribute("src")
                            except:
                                imageURL = self.browser.find_element(By.XPATH,'//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[3]/div/a/img').get_attribute("src")

                            if imageURL != previewImageURL and 'encrypted' not in imageURL and 'http' in imageURL:
                                print("actual URL", imageURL)
                                break
                            else:
                                # making a timeout if the full res image can't be loaded
                                currentTime = time.time()

                                if currentTime - timeStarted > 9:
                                    print("Timeout! Will download a lower resolution image and move onto the next one")
                                    break

                        # Downloading image
                        if imageURL != None and imageURL not in img_list:
                            img_list.append(imageURL)
                    except:
                        print('没有打开，下一个')
                        pass
                else:
                    pass
            sleep(2)
            self.swipe_up()
            buty = self.browser.find_element(By.XPATH, '//*[@id="{}"]/div[1]/span/span[1]/div/a'.format(iiiiii))
            # self.swipe_down(0.5)
            print(buty)
            buty.click()
            self.browser.implicitly_wait(5)
            sleep(2)
        sleep(2)
        print(len(img_list))
        a = np.array(img_list)
        np.save('{}.npy'.format(url_name), a)
        return self.browser,img_list
        self.browser.close()

if __name__ == "__main__":
    VK_CODE = {'enter': 0x0D, 'down_arrow': 0x28}
    chromedriver_path = "E:\xxxxxxx/chromedriver.exe"  # Change to the full path address of your chromedriver
    url_data = {
        'villa': 'https://www.google.com/search?q=villa&tbm=isch&ved=2ahUKEwj615D77Yb7AhUgoY4IHTcvA8AQ2-cCegQIABAA&oq=villa&gs_lcp=CgNpbWcQDDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgARQAFgAYMUHaABwAHgAgAHwAYgB8AGSAQMyLTGYAQCqAQtnd3Mtd2l6LWltZ8ABAQ&sclient=img&ei=B9tdY7q4MqDCuvQPt96MgAw&bih=730&biw=1536',
        'Construction site': 'https://pic.sogou.com/pics?query=%E5%BB%BA%E7%AD%91%E5%B7%A5%E5%9C%B0&w=05009900',
        'construction worker': 'https://www.google.com/search?q=construction+worker&tbm=isch&ved=2ahUKEwjWz9L3_oz7AhVj_TgGHe6MDm8Q2-cCegQIABAA&oq=construction+worker&gs_lcp=CgNpbWcQDDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB5QrwVYrwVgrhFoAHAAeACAAYABiAH7AZIBAzAuMpgBAKABAaoBC2d3cy13aXotaW1nwAEB&sclient=img&ei=IhJhY9a2FeP64-EP7pm6-AY&bih=710&biw=1019&hl=zh-CN',
        'Scaffolding': 'https://www.google.com/search?q=Scaffolding&tbm=isch&ved=2ahUKEwjn6vmrjo37AhX4itgFHcgiC80Q2-cCegQIABAA&oq=Scaffolding&gs_lcp=CgNpbWcQDDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQ6BAgAEB46BggAEAcQHlDnDljnDmCdHGgAcAB4AIABfYgB9QGSAQMwLjKYAQCgAQGqAQtnd3Mtd2l6LWltZ8ABAQ&sclient=img&ei=SiJhY-edI_iV4t4PyMWs6Aw&bih=710&biw=1019&hl=zh-CN',
        'steel bar': 'https://www.google.com/search?q=steel+bar&tbm=isch&ved=2ahUKEwjYjMa2jo37AhX4i9gFHV4hALUQ2-cCegQIABAA&oq=steel+bar&gs_lcp=CgNpbWcQDDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgQIABAeMgQIABAeMgQIABAeMgQIABAeMgQIABAeUJcGWJcGYIoRaABwAHgAgAGFAogB8gKSAQUwLjEuMZgBAKABAaoBC2d3cy13aXotaW1nwAEB&sclient=img&ei=YCJhY9jcMPiX4t4P3sKAqAs&bih=710&biw=1019&hl=zh-CN',
        'Concrete block': 'https://www.google.com/search?q=Concrete+block&tbm=isch&ved=2ahUKEwiltuK_jo37AhUQkdgFHanxCTkQ2-cCegQIABAA&oq=Concrete+block&gs_lcp=CgNpbWcQDDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgQIABAeMgQIABAeMgQIABAeMgQIABAeMgQIABAeOgYIABAHEB5QtgVYtgVgthBoAHAAeACAAYYBiAGDApIBAzAuMpgBAKABAaoBC2d3cy13aXotaW1nwAEB&sclient=img&ei=dCJhY6WsCJCi4t4PqeOnyAM&bih=710&biw=1019&hl=zh-CN',
        'safety hat': 'https://www.google.com/search?q=safety+hat&tbm=isch&ved=2ahUKEwilmoTIjo37AhVTk9gFHQ8UAdMQ2-cCegQIABAA&oq=safety+hat&gs_lcp=CgNpbWcQDDIFCAAQgAQyBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB4yBAgAEB46BggAEAcQHlC-A1i-A2CJDmgAcAB4AIABhAGIAYMCkgEDMC4ymAEAoAEBqgELZ3dzLXdpei1pbWfAAQE&sclient=img&ei=hSJhY-XDHNOm4t4Pj6iEmA0&bih=710&biw=1019&hl=zh-CN',
        'Tunnel': 'https://www.google.com/search?q=Tunnel&tbm=isch&ved=2ahUKEwjGvOTPjo37AhUFj9gFHdGgDUYQ2-cCegQIABAA&oq=Tunnel&gs_lcp=CgNpbWcQDDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQ6BggAEAcQHlCXA1iXA2DZDWgAcAB4AIABeYgB8gGSAQMwLjKYAQCgAQGqAQtnd3Mtd2l6LWltZ8ABAQ&sclient=img&ei=lSJhY4aeLIWe4t4P0cG2sAQ&bih=710&biw=1019&hl=zh-CN',
    }

    path_url = None

    list_name = ['steel bar','Scaffolding']
    if path_url == None:
        for i in list_name:
            a = taobao_infos()
            browser,img_list = a.crawl_good_data(i)   #craw data
