#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/12/5 21:28
# @Author : J.wang
# @Version：V 0.1
# @File : qz_ApiRetained.py
# @desc : （3) 具体业务接口  接口调用固定写死入参请求
import requests,time,datetime,redis,hashlib
time = str(int(time.time()*1000))
print(time)
# 连接 redis
r = redis.Redis(host='localhost', port=6379, db=1, decode_responses=True)

# MD5 数据加工
def str_md5(str = ''):
    md = hashlib.md5()
    md.update(str.encode(encoding="utf-8"))
    return  md.hexdigest()

# 定义方法传参形式
def gateway(url,appKey,appSecret):
    # 打印参数信息
    print('url：'+url+'\nappKey：'+appKey+'\nappSecret：'+appSecret)
    # todo 准备参数
    # (1) appKey  (参数自带)
    # (2) requestTime （获取当前时间戳）
    requestTime = time
    # (3) sign
    str = appKey+appSecret+requestTime
    sign = str_md5(str)
    # (4) 业务参数  (查询接口配置信息)
    # 组合参数
    params = {"appKey":appKey,"sign":sign,"requestTime":requestTime,"cardId":"330881198410085911"}
    response = requests.get(url,params).json()
    if response != None and response['code'] == '00':
        print(response)
        # 存储数据

# 调用方法 刷新请求密钥方法
if __name__ == "__main__":
    url = 'https://dw.qz.gov.cn/gateway/api/001008013008001/dataSharing/p6b45bR28ejPr6z3.htm?'
    appKey = '46eb7734001641048cd20cf15f18610a'
    appSecret = r['requestSecret']
    gateway(url,appKey,appSecret)
