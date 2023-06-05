#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2022/10/9 11:00
# @Author : hc.guan
# @Version：V 0.1
# @File : qzApi_BatchRetainedToTable.py
# @desc : 全省健康码调用脚本


import requests, json, datetime, hashlib
import time, redis

time_stamp = str(int(time.time() * 1000))
# 连接redis
r = redis.Redis(host='127.0.0.1',port=6379,db=0)

#sign 签名
def md5value(appKey,appSecret):

    str = appKey + appSecret + time_stamp
    sign = hashlib.md5()
    sign.update(str.encode("utf-8"))
    sign = sign.hexdigest()
    return sign

# 刷新密钥
def get_refresh(appKey,sign):
    url = 'http://interface.zjzwfw.gov.cn/gateway/app/refreshTokenByKey.htm'
    params = {
        'appKey':appKey,
        'sign':sign,
        'requestTime':time_stamp
    }
    response = requests.get(url,params)
    if response.status_code == 200:
        response = response.json()
        print("接口请求结束--------------------------------------------------")
        return response
    else:
        print("接口请求失败--------------------------------------------------")

# 请求密钥
def get_secret(appKey,sign):
    url = 'http://interface.zjzwfw.gov.cn/gateway/app/refreshTokenBySec.htm'
    params = {
        'appKey': appKey,
        'sign': sign,
        'requestTime': time_stamp
    }
    response = requests.get(url,params)
    if response.status_code == 200:
        response = response.json()
        requestSecret = response['datas']['requestSecret']
        print("接口请求结束--------------------------------------------------")
        return requestSecret
    else:
        print("接口请求失败--------------------------------------------------")


# 健康码查询
def jkm_query(appKey,sign):
    url = 'https://interface.zjzwfw.gov.cn/gateway/api/001003001/dataSharing/uU4lb0350783d2fa.htm'
    params = {
        'appKey': appKey,
        'sign': sign,
        'requestTime': time_stamp,
        'sfzh': '331004200108181421'
    }
    response_jkm = requests.get(url,params)
    print(response_jkm.json())
    return response_jkm.status_code


'''main 方法：主要方法是用于启动 - 调用方法'''
if __name__ == "__main__":
    # todo 1 程序开始时间
    startTime = datetime.datetime.now()
    print('\033[0;33;40m Program starts running 。。。 \033[0m')

    # todo 2 调用刷新密钥方法
    appKey = 'A330881406627202107016701'
    appSecret = "e011fbb67ccb441c93dc18e9b2f2d86b"

    r.rpush('sign',md5value(appKey, appSecret))
    refreshSecret = get_refresh(appKey, r.lindex('sign', -1).decode())

    # 有效期失效 重新获取签名
    if get_refresh(appKey, r.lindex('sign', -1).decode())['code'] != 200:
        refreshSecret = get_refresh(appKey, r.lindex('sign', -1).decode())['datas']['refreshSecret']
        r.rpush('sign', md5value(appKey, refreshSecret))
        requestSecret = get_secret(appKey, r.lindex('sign', -1).decode())

        r.rpush('sign', md5value(appKey, requestSecret))
        jkm_query(appKey, r.lindex('sign', -1).decode())

    # 15分钟有效期内
    else:
        jkm_query(appKey, r.lindex('sign', -1).decode())


    # todo 3 程序结束时间 并输出总耗时
    endTime = datetime.datetime.now()
    durTime = '\033[0;33;40m funtion time use:%dms \033[0m' % (
            (endTime - startTime).seconds * 1000 + (endTime - startTime).microseconds / 1000)
    print(durTime)
