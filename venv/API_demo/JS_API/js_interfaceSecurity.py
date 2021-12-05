#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/12/5 21:31
# @Author : J.wang
# @Version：V 0.1
# @File : js_interfaceSecurity.py
# @desc : (2)刷新请求密钥接口

import requests
from js_appsecert import test_api
def request_interfaceSecurity(appsecert):
    interfaceSecurity_url = "http://szgg.jiangshan.gov.cn:81/interfaceSecurity"   # 接口地址:请求密钥
    # body = {"refreshSecret": appsecert['refreshSecret'],"appKey":"acimwoFCVSz7JXJeoXw7","requestTime": appsecert['requestTime']}
    body_2 = {"refreshSecret": "b7d78d48a7a2a0b95b56abe946bb4e48","appKey":"acimwoFCVSz7JXJeoXw7","requestTime": "1638715688647"}
    headers ={'Content-Type':'application/json'}
    r = requests.post(interfaceSecurity_url, json=body_2, headers=headers)  # verify = False 忽略SSH 验证
    print(r)
    if r == None and str(r.json()['code']) == '0':
        print("2刷新密钥请求成功！！！")
        requestSecret = r.json()['data']['requestSecret']
        requestTime = r.json()['data']['requestTime']
        print(requestSecret+' ------------------- '+str(requestTime))
    # return {'requestSecret':requestSecret,'requestTime':requestTime}
if __name__ == '__main__':
    print('开始请求：请求密钥')
    a = test_api.request_appsecert()
    print(a['refreshSecret'])
    print(request_interfaceSecurity(a))
    print('结束请求：请求密钥')