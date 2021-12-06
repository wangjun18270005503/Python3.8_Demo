#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/12/5 21:28
# @Author : J.wang
# @Version：V 0.1
# @File : qz_refreshTokenByKey.py
# @desc : （1）刷新密钥
import requests, time, datetime, hashlib, redis
time = str(int(time.time()*1000))
'''
print(time)
ByKey_url = 'https://dw.qz.gov.cn/gateway/app/refreshTokenByKey.htm?'  #接口地址：刷新密钥
params = {
    "appKey":"46eb7734001641048cd20cf15f18610a",
    "sign":"686cb9d6be45b1605c4055c15a8109c7",
    "requestTime":"1638762409405"
}
a = requests.get(ByKey_url,params=params)
print(a.text)
'''

# MD5 数据加工
def str_md5(str = ''):
    md = hashlib.md5()
    md.update(str.encode(encoding="utf-8"))
    return  md.hexdigest()

# 定义方法传参形式
def refreshTokenByKey(url,appKey,appSecret):
    # 打印参数信息
    print('url：'+url+'\nappKey：'+appKey+'\nappSecret：'+appSecret)
    # todo 准备参数
    # (1) appKey  (参数自带)
    # (2) requestTime （获取当前时间戳）
    requestTime = time
    # (3) sign
    str = appKey+appSecret+requestTime
    sign = str_md5(str)
    # 组合参数
    params = {"appKey":appKey,"sign":sign,"requestTime":requestTime}
    response = requests.get(url,params).json()
    if response != None and response['code'] == '00':
        print(response)
        # 存储至redis
        r = redis.Redis(host='localhost', port=6379, db=1, decode_responses=True)
        r.set('refreshSecret', response['datas']['refreshSecret'])  # 设置 name 对应的值

# 调用方法 刷新请求密钥方法
if __name__ == "__main__":
    url = 'https://dw.qz.gov.cn/gateway/app/refreshTokenByKey.htm?'
    appKey = '46eb7734001641048cd20cf15f18610a'
    appSecret = '31b4020cd1c6419bb48bd27e6b239282'
    refreshTokenByKey(url,appKey,appSecret)
    print('md5：'+str_md5('1111'))
