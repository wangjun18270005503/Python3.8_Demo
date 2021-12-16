#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/12/5 16:54
# @Author : J.wang
# @Version：V 0.1
# @File : xz_yzm.py
# @desc :

import time
from selenium import webdriver
from PIL import Image
coding='utf-8'
options = webdriver.ChromeOptions()
options.add_argument('ignore-certificate-errors')
#driver = webdriver.Firefox(executable_path=r'C:\Program Files\Mozilla Firefox\geckodriver.exe')
driver = webdriver.Chrome(executable_path=r'../comment/chromedriver_win32/chromedriver.exe', options=options)
driver.maximize_window()
driver.implicitly_wait(6)
driver.get("https://220.191.236.163:6443/index.php/")     #此处为url地址
time.sleep(1)
driver.get_screenshot_as_file('./image/截图.png')
imgelement = driver.find_element_by_class_name('capimg')  #定位验证码
# /html/body/form/div[3]/div[3]/div/ul/li[4]/img
location = imgelement.location
# location = imgelement.location_once_scrolled_into_view
size = imgelement.size
a1 = tuple(location.values())   #(x,y)
a2 = tuple(size.values())   #(height,width)
print(location)
print(size)
# driver.close()
rangle = (a1[0]*1.25,a1[1]*1.25,a1[0]*1.25+a2[1]*1.25,a1[1]*1.25+a2[0]*1.05)    #(x,y,x+width,y+height)  注意本机设置的缩放比例为125%，故所有元素*1.25
print(rangle)
i = Image.open('../image/截图.png')
frame4 = i.crop(rangle)
frame4.save('./image/验证码1.png')