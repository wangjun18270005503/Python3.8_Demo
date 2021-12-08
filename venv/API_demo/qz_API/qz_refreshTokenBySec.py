#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/12/5 21:26
# @Author : J.wang
# @Version：V 0.1
# @File : qz_refreshTokenBySec.py
# @desc : （2）请求密钥
import requests, time, datetime, hashlib, redis

time = str(int(time.time() * 1000))
print(time)
'''
# https://dw.qz.gov.cn/gateway/app/refreshTokenBySec.htm?appKey=46eb7734001641048cd20cf15f18610a&sign=e5989b729e6e39b97ab9e37942097cd9&requestTime=1638776323145
BySec_url = 'https://dw.qz.gov.cn/gateway/app/refreshTokenByKey.htm?'  #接口地址：刷新密钥
params = {
    "appKey":"46eb7734001641048cd20cf15f18610a",
    "sign":"e5989b729e6e39b97ab9e37942097cd9",
    "requestTime":"1638776323145"
}
a = requests.get(BySec_url,params=params)
print(a.text)
'''
# 连接 redis
r = redis.Redis(host='localhost', port=6379, db=1, decode_responses=True)


# MD5 数据加工
def str_md5(str=''):
    md = hashlib.md5()
    md.update(str.encode(encoding="utf-8"))
    return md.hexdigest()


# 定义方法传参形式
def refreshTokenBySec(url, appKey):
    appSecret = r['refreshSecret']
    # 打印参数信息
    print('url：' + url + '\nappKey：' + appKey + '\nappSecret：' + appSecret)
    # todo 准备参数
    # (1) appKey  (参数自带)
    # (2) requestTime （获取当前时间戳）
    requestTime = time
    # (3) sign
    str = appKey + appSecret + requestTime
    sign1 = str_md5(str)
    # 组合参数
    params = {"appKey": appKey, "sign": sign1, "requestTime": requestTime}
    response = requests.get(url, params).json()
    print(response)
    if response != None and response['code'] == '00':
        requestSecret = response['datas']['requestSecret']
        r.set('requestSecret', requestSecret)  # 设置 name 对应的值
        print('requestSecret：' + requestSecret)


# 调用方法 刷新请求密钥方法
if __name__ == "__main__":
    url = 'https://dw.qz.gov.cn/gateway/app/refreshTokenBySec.htm?'
    appKey = '46eb7734001641048cd20cf15f18610a'
    # appSecret = r['refreshSecret']
    refreshTokenBySec(url, appKey)
