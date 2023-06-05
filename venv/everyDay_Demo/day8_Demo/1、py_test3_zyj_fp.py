#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2022/9/30 17：00
# @Author :
# @Version：V 0.1
# @File :
# @desc : 2022/9/30 全省健康码查询get\post 接口练习

# 优化问题：
# 1、利用requestSecret 15分钟时效性
# 建议：将密钥相关信息存储到redis 或者 数据库(两个字段，一个放密钥；一个放时间（直接相减<=15min）)中
# （每次先去读取，当前最新的密钥，然后校验分析，是否失效，若是失效再进行调用二、一）、
# 2、异常情况处理：当返回不成功时，例如return ref_dict["datas"]['refreshSecret']

import requests
import datetime
import time
# 在python3中使用hashlib模块进行md5操作
import hashlib
import redis
# 本地连接，创建数据库连接对象；db 表示当前选择的库，其参数值可以是 0-15
r = redis.Redis(host='127.0.0.1', port=6379, db=0)
appKey = "A330881406627202107016701"

# 字符串进行md5加密
def md5(str):
    # 创建md5对象
    m = hashlib.md5()
    m.update(str.encode("utf8"))
    return m.hexdigest()

# 获得13位时间戳
def get_time_stamp13():
    # 生成13时间戳   eg:1540281250399895
    datetime_now = datetime.datetime.now()
    # 10位，时间点相当于从UNIX TIME的纪元时间开始的当年时间编号
    date_stamp = str(int(time.mktime(datetime_now.timetuple())))
    # 3位，微秒
    data_microsecond = str("%06d" % datetime_now.microsecond)[0:3]
    date_stamp = date_stamp + data_microsecond
    return str(date_stamp)

def get_way(app_getsecret, u):
    # 配置时间戳
    mkt = get_time_stamp13()
    appSecret = app_getsecret
    str_md5 = appKey + appSecret + str(mkt)
    sign = md5(str_md5)
    url = u
    parmas = {
        "appKey": appKey,
        "sign": sign,
        "requestTime": mkt
    }
    headers = {}
    response = requests.get(url=url, headers=headers, params=parmas)
    response.encoding = 'utf-8'
    req_dict = response.json()
    return req_dict

def post_way(app_postsecret):
    appSecret = app_postsecret
    mkt = get_time_stamp13()
    str_md5 = appKey + appSecret + str(mkt)
    sign = md5(str_md5)
    data_dict = {
        "appKey": appKey,
        "sign": sign,
        "requestTime": mkt,
        "sfzh": "500236200108211304"
    }
    url = "https://interface.zjzwfw.gov.cn/gateway/api/001003001/dataSharing/uU4lb0350783d2fa.htm?"
    headers = {}
    response = requests.post(url=url, headers=headers, data=data_dict)
    rep_obj = response.json()
    return rep_obj

def refresh_key():
    ref_dict = get_way("e011fbb67ccb441c93dc18e9b2f2d86b",
                       "http://interface.zjzwfw.gov.cn/gateway/app/refreshTokenByKey.htm?")
    # print("ref")
    # print(ref_dict)
    return ref_dict["datas"]['refreshSecret']

def request_key():
    ref_sec = refresh_key()
    req_dict = get_way(ref_sec, 'http://interface.zjzwfw.gov.cn/gateway/app/refreshTokenBySec.htm?')
    if (req_dict['code'] == "00"):
        # 将得到的密钥存入redis（rpush,从尾部取）
        r.rpush('req_list', req_dict["datas"]['requestSecret'])
        # print("req")
        # print(req_dict)
        return req_dict["datas"]['requestSecret']
    else:
        print('请求错误')

def JKM_search():
    # 1、读取最新，2、校验分析是否失效，若是失效再进行调用上面步骤
    se_sec = r.lindex('req_list', -1).decode()
    # se_sec = "8aaf320622ef407f96e745fadb72eab1"
    se_check = post_way(se_sec)
    if (se_check['code'] == "00"):
        print(se_check)
    else:
        print("请求密钥失效,现重取")
        req = request_key()
        se_dict = post_way(req)
        print(se_dict)

if __name__ == "__main__":
    print("\033[0;32m%s\033[0m" % u"===================start===================")
    d1 = datetime.datetime.now()
    print(u"开始时间：", d1)
    #初次运行，req_list里没有请求密钥；需要初始化
    if (r.lrange('req_list', 0, -1) == []):
        request_key()
    JKM_search()
    d2 = datetime.datetime.now()
    print(u"结束时间：", d2)
    print("\033[0;31m%s\033[0m" % u"总共耗时：", d2 - d1)
    print("\033[0;32m%s\033[0m" % u"===================stop===================")