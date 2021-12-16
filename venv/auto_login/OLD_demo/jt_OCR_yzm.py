#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/12/5 17:35
# @Author : J.wang
# @Version：V 0.1
# @File : jt_ORC_yzm.py
# @desc :

import time,json,requests,base64,time,datetime,os
from selenium import webdriver
from PIL import Image
coding='utf-8'
# 系统地址
url = "https://220.191.236.163:6443/index.php/"
OCR_api_post_url = "http://www.bingtop.com/ocr/upload/"  #识别地址
options = webdriver.ChromeOptions()
options.add_argument('ignore-certificate-errors')
#driver = webdriver.Firefox(executable_path=r'C:\Program Files\Mozilla Firefox\geckodriver.exe')
driver = webdriver.Chrome(executable_path=r'../comment/chromedriver_win32/chromedriver.exe', options=options)
driver.maximize_window()
driver.implicitly_wait(6)
driver.get(url)     #此处为url地址
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
frame4.save('./image/验证码.png')
# 开始识别
img_url = r'./image/验证码.png'  # img_url，图片存放路径
with open(img_url,'rb') as pic_file:
    img64=base64.b64encode(pic_file.read())  # 读取图片，并获取图片的base64数据
params = {
    "username": "%s"%"wangjun",
    "password": "%s"%"wangjun@12138",
    "captchaData": img64,
    "captchaType": 1003
}
print(params)
response = requests.post(OCR_api_post_url, data=params)
dictdata=json.loads(response.text)
if dictdata != 'null':
    verification_Code = dictdata["data"]["recognition"]
    print('识别到的验证码为：'+verification_Code)