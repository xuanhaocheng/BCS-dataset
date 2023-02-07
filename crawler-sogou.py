

# -*- coding: utf-8 -*-
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



# 定义一个taobao类
class taobao_infos:

    def __init__(self):
        options = webdriver.ChromeOptions()
        #options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2}) 
        options.add_experimental_option('excludeSwitches',
                                        ['enable-automation'],)  # This step is very important. It is set to developer mode to prevent Selenium from being recognized by major websites
        #options.add_argument("--headless")  #This step adds headless mode. After the program debugging is qualified, you can add this step. So the computer can do other things when crawling data.

        self.browser = webdriver.Chrome(executable_path=chromedriver_path, options=options)
        self.browser.implicitly_wait(5)
        self.wait = WebDriverWait(self.browser, 20)  # The timeout duration is 20s
    # 模拟向下滑动浏览  Simulate sliding down
    def swipe_down(self, second):
        for i in range(int(second / 0.1)):
            js = "var q=document.documentElement.scrollTop=" + str(300 + 200 * i)
            self.browser.execute_script(js)
            sleep(0.1)
        js = "var q=document.documentElement.scrollTop=100000"
        self.browser.execute_script(js)
        sleep(0.2)

    # 爬取数据  Crawl data
    def crawl_good_data(self,url_name):
        url_data = {
                     '建筑工地板房':'https://pic.sogou.com/pics?query=%E5%BB%BA%E7%AD%91%E5%B7%A5%E5%9C%B0%E6%9D%BF%E6%88%BF&w=05009900',
                     '建筑工地彩钢房':'https://pic.sogou.com/pics?query=%E5%BB%BA%E7%AD%91%E5%B7%A5%E5%9C%B0%E5%BD%A9%E9%92%A2%E6%88%BF&w=05009900',
                     '建筑工地活动房':'https://pic.sogou.com/pics?query=%E5%BB%BA%E7%AD%91%E5%B7%A5%E5%9C%B0%E6%B4%BB%E5%8A%A8%E6%88%BF&w=05009900',
                     }
        if os.path.exists(url_name) ==False:
            os.makedirs(url_name)
        self.browser.get(url_data.get(url_name))

        # The essence is to simulate the manual downward browsing of goods, that is, to simulate the sliding operation to prevent being recognized as a robot
        self.swipe_down(150)
        name = self.browser.find_elements(By.XPATH,'// *[ @ id = "picPc"] / div / div[2] / div / ul / li/ div / a[1] / img')
        print("len11", len(name))
        n = 0
        m = 0
        img_list = []
        for item in name:
            m+=1
            if m>=0: #1640
            #print("item.text",item)
                if n%10 == 0:
                    sleep(0.5)
                if n % 100 == 0:
                    print(n)
                try:
                    item.click()
                    self.browser.switch_to.window(self.browser.window_handles[-1])
                    sleep(0.6)
                    try:
                         img_url = self.browser.find_element(By.XPATH,'//*[@id="imgArea"]/div[3]/div/div/a/img').get_attribute("drag-img")   #因为只有find_element才有get_attribute
                    except:
                         img_url = None
                    print("{}/m".format(url_name), m)
                    print("img_url", img_url)
                    self.browser.close()
                    sleep(1)
                    self.browser.switch_to.window(self.browser.window_handles[0])

                except:
                    print("遇到广告跳到下一个")
                    img_url = None
                    pass

                if img_url != None and img_url  not in img_list:
                    img_list.append(img_url)
                    with open("{}/%d.jpg".format(url_name)%n,"wb") as file:
                        try:
                            file.write(requests.get(img_url).content)
                        except:
                            pass

                else:
                    n -= 1
                    pass
                n += 1
            print(n)
            print(len(img_list))
        self.browser.close()




if __name__ == "__main__":

    list_url = ['建筑工地板房','建筑工地彩钢房'] #Specify the keywords to be downloaded here, the previous url_ Data needs to fill in a complete URL
    for i in list_url:
        chromedriver_path = "E:/xxxxxxx/chromedriver.exe"  # Change to the full path address of your chrome driver. The version of chrome driver should match the version of chrome.
        a = taobao_infos()
        a.crawl_good_data(i)   #craw data




