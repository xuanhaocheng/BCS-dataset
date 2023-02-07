
'''
The purpose of this code is to use the selenium module to call chrome to download the npy format file, which contains the image URL.
Use the win32 module to call the mouse and keyboard to save.
When calling the win32 module, the input method should be set to English, otherwise there will be a problem when you press OK on the final analog keyboard.
'''

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
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import win32api
import win32con
import numpy as np
import win32gui
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

# Define a taobao class
def taobao_infos():
    options = webdriver.ChromeOptions()


    options.add_experimental_option('excludeSwitches',
                                    ['enable-automation'], ) # This step is very important. It is set to developer mode to prevent Selenium from being recognized by major websites
    #options.add_argument("--headless")

    browser = webdriver.Chrome(executable_path=chromedriver_path, options=options)
    wait = WebDriverWait(browser, 20)

    return browser

    # Define keyboard press events
def keyDown(keyName):
    win32api.keybd_event(VK_CODE[keyName], 0, 0, 0)

# Define keyboard release events
def keyUp(keyName):
    win32api.keybd_event(VK_CODE[keyName], 0, win32con.KEYEVENTF_KEYUP, 0)

def get_chrome_window_center_coordinate(): #Find the positive center coordinate of the open Chrome window
    chrome_hwnd = win32gui.FindWindow("Chrome_WidgetWin_1", None)
    if chrome_hwnd:
        left, top, right, bottom = win32gui.GetWindowRect(chrome_hwnd)
        width = right - left
        height = bottom - top
        x = left + width // 2
        y = top + height // 2
        return (x, y)
    else:
        return None

def download_image(driver, urls):
    chrome_center_coordinate = get_chrome_window_center_coordinate() #Find the coordinates of the center of the chrome window
    i = 0
    for url in urls:
        i += 1
        if i >= 0: #len(urls) 1074
            print(url)
            try:
                start_time = time.time()
                driver.get(url)
                #print(len(driver.window_handles))
                if len(driver.window_handles) ==2 :
                    driver.switch_to.window(driver.window_handles[-1])
                    sleep(1)
                    driver.close()
                    sleep(1)
                    driver.switch_to.window(driver.window_handles[0])
                # image=driver.find_element_by_xpath('//*[@id="currentImg"]')#定位图片所在的元素
                image = driver.find_element(By.XPATH, '/html/body/img')
                action = ActionChains(driver).move_to_element(image)
                # ActionChains(driver).context_click(image).perform()

                win32api.SetCursorPos(chrome_center_coordinate)   # Move the mouse to the coordinate of the center of chrome
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 200, 200, 0, 0)
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 200, 200, 0, 0)
                action.context_click(image).perform()  # Right-click on a picture element
                time.sleep(0.8)  # Prevent pictures from not being loaded

                win32api.keybd_event(86, 0, 0, 0)  # Call and press the keyboard function, and pass in the parameter "86" for the function, that is, "v"
                win32api.keybd_event(86, 0, win32con.KEYEVENTF_KEYUP, 0)  # Release keyboard "V"
                time.sleep(0.4)
                url_data = {'0': '48', '1': '49', '2': '50', '3': '51', '4': '52', '5': '53', '6': '54', '7': '55',
                            '8': '56', '9': '57'}

                bbbb = list(str(i))
                sleep(0.2)
                for i_number in bbbb:
                    # print(i_number)
                    # print(int(url_data.get(i_number)))
                    win32api.keybd_event(int(url_data.get(i_number)), 0, 0, 0)  # Call the function of pressing the keyboard, and pass in parameters for the function, corresponding to the name of the photo
                    win32api.keybd_event(int(url_data.get(i_number)), 0, win32con.KEYEVENTF_KEYUP, 0)
                win32api.keybd_event(190, 0, 0, 0)
                win32api.keybd_event(190, 0, win32con.KEYEVENTF_KEYUP, 0)
                #sleep(0.05)
                win32api.keybd_event(74, 0, 0, 0)
                win32api.keybd_event(74, 0, win32con.KEYEVENTF_KEYUP, 0)
                #sleep(0.05)
                win32api.keybd_event(80, 0, 0, 0)
                win32api.keybd_event(80, 0, win32con.KEYEVENTF_KEYUP, 0)
                #sleep(0.05)
                win32api.keybd_event(71, 0, 0, 0)
                win32api.keybd_event(71, 0, win32con.KEYEVENTF_KEYUP, 0)  #Call the press keyboard function. Pass in the parameter '. jpg'
                time.sleep(0.4)
                keyDown('enter')  # Press the "Confirm" button, sWhen calling the win32 module, the input method should be set to English, otherwise there will be a problem when you press OK on the final analog keyboard.
                keyUp('enter')  # Release the confirmation button
                time.sleep(0.1)  # Wait 0.1 seconds
                print("{}/{}张图片下载完成".format(i,len(urls)))
            except:
                print("{}/{}张图片下载失败".format(i,len(urls)))
                continue



if __name__ == "__main__":
    VK_CODE = {'enter': 0x0D, 'down_arrow': 0x28}
    chromedriver_path = r"E:\xxxxxxxx/chromedriver.exe"  # Change to the full path address of your chromedriver
    path_url = None
    list_name = ['steel bar','Scaffolding'] # Change here to the name of the downloaded npy file

    if path_url ==None:
        for i in list_name:
            ii = 0
            path = r'E:\BCS_dataset\BCS-dataset/'+str(i)+'.npy' # This is changed to the absolute address of the npy file
            img_list = np.load(path)
            browser = taobao_infos()
            download_image(browser, img_list)



