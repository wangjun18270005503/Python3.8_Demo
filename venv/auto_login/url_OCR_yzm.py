#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/12/5 12:53
# @Author : J.wang
# @Version：V 0.1
# @File : yzm.py
# @desc :  自动识别验证码
'''
    通过 冰拓 识别
        URL：http://bingtop.com/account/login/
        username：wangjun
        password：wangjun@12138
'''
import json
import requests,base64,time,datetime  # http客户端
import os  # 创建文件夹
from PIL import Image
t = str(int(round(time.time() * 1000))) #毫秒级时间戳
api_post_url = "http://www.bingtop.com/ocr/upload/"  #识别地址
yzm1_url = 'http://220.191.236.195:9101/verifyCode?timestamp='+t   #人民大调解
yzm2_url = 'https://220.191.236.163:6443/captcha/1638692164.7482.jpg'  #新堡垒机 验证码网址，可以根据需求更换
IMAGE_URL = "http://jwgl.cqjtu.edu.cn/jsxsd/verifycode.servlet?t=0.33489178693749055"
os.makedirs('./image/', exist_ok=True)
def request_download():
    r = requests.get(yzm1_url)
    # r = requests.post(yzm2_url)
    with open('./image/img.png', 'wb') as f:
        f.write(r.content)
        print('下载文件')
try:
    request_download()
    print('download img')
    # im = Image.open('./image/img.png')
    # im.show()
except:
    print('download img error!')

# 需安装第三方requests
# img_url，图片存放路径
# 读取图片，并获取图片的base64数据
img_url = r'./image/img.png'
with open(img_url,'rb') as pic_file:
    img64=base64.b64encode(pic_file.read())
params = {
    "username": "%s"%"wangjun",
    "password": "%s"%"wangjun@12138",
    "captchaData": img64,
    "captchaType": 1001
}
print(params)
response = requests.post(api_post_url, data=params)

dictdata=json.loads(response.text)
if dictdata != 'null':
    print('识别到的验证码为：'+dictdata["data"]["recognition"])





