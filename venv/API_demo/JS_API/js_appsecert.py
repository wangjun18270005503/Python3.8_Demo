#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/12/5 21:30
# @Author : J.wang
# @Version：V 0.1
# @File : js_appsecert.py
# @desc : （1）获取刷新密钥接口

import requests
class  test_api():
    def request_appsecert():
        secert_url = "http://szgg.jiangshan.gov.cn:81/appsecert"  # 接口地址:刷新密钥
        body = {"appSecret":"BMZFIqnp3kVp4fhHWmxL","appKey":"acimwoFCVSz7JXJeoXw7"}
        headers={'Content-Type':'application/json'}
        r = requests.post(secert_url, json=body, headers=headers)  # verify = False 忽略SSH 验证
        if len(r.text) != 0 and str(r.json()['code']) == '0':
            print("刷新密钥请求成功！！！")
            refreshSecret = r.json()['data']['refreshSecret']
            requestTime = r.json()['data']['requestTime']
            print(refreshSecret+' ------------------- '+str(requestTime))
        return {'refreshSecret':refreshSecret,'requestTime':str(requestTime)}
if __name__ == '__main__':
    print('开始请求：刷新密钥')
    print(test_api.request_appsecert())
    print('结束请求：刷新密钥')