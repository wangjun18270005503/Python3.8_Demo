# -*- coding: utf-8 -*- 
# @Project ：Git_Python3.8_Demo 
# @Time : 2022/1/10 17:05 
# @Author : J.wang 
# @Version：V 0.1 
# @File : GetScreenedPersonList_demo1.py
# @Software: PyCharm
# @desc : 获取’浙江省全员新冠病毒核酸检测平台‘当中 筛选清单

import re,os,base64,datetime,urllib3
import image
import pymysql, json, math, random
import requests, time, redis, hashlib
from PIL import Image

requestTime = str(int(time.time() * 1000))
print('当前请求时间戳（毫秒）：' + requestTime)
# 连接 生成服务器redis
# r = redis.Redis(host='10.27.235.209', port=9004, db=6, password='sx123456', decode_responses=True)
# 连接 测试服务器redis:
# r = redis.Redis(host='10.50.207.215', port=6379, db=6, password='sx123456', decode_responses=True)
# 连接 本地redis
r = redis.Redis(host='localhost', port=6379, db=1, decode_responses=True)
api_post_url = "http://www.bingtop.com/ocr/upload/"  # 识别地址
yzm_url = 'https://yknaes.wsjkw.zj.gov.cn:16659/api/user/GetCapture?id=123737.84126937944'
# yzm_url = 'http://jwgl.cqjtu.edu.cn/jsxsd/verifycode.servlet?t=0.33489178693749055'
login_url = 'https://yknaes.wsjkw.zj.gov.cn:16659/api/User/UserLogin?LOGIN_ID=H34&PASSWARD=ba6bb99d06d005ce169ad5c0b917384d&captureId=123737.84126937944'
list_url = 'https://yknaes.wsjkw.zj.gov.cn:16659/api/DataQuery/GetScreenedPersonList?hospitalId=H34&level1=浙江省&level2=衢州市&level3=江山市&QUEUE_SIGN=0&startTime=2022-01-10 00:00:00&endTime=2022-01-10 23:59:59'






# 需安装第三方requests
# img_url，图片存放路径
# 读取图片，并获取图片的base64数据
# img_url = r'./image/yzm.png'
# with open(img_url, 'rb') as pic_file:
#     img64 = base64.b64encode(pic_file.read())
# params = {
#     "username": "%s" % "wangjun",
#     "password": "%s" % "wangjun@12138",
#     "captchaData": img64,
#     "captchaType": 1001
# }
# print(params)
# response = requests.post(api_post_url, data=params)
#
# dictdata = json.loads(response.text)
# if dictdata != 'null':
#     print('识别到的验证码为：' + dictdata["data"]["recognition"])
