#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2022/10/9 9:25
# @Author : zyj
# @Version：V 0.1
# @File : py_test3_zyj_2.py
# @desc :2.0版需求：健康码接口可实现模拟每天8:00~19:00 时间段内，每小时内有随机0~5个不同人员调用接口。
# 实现思路：
# 1、脚本启用定时调度，每分钟执行一次。
# 2、在main方法中，每次执行时判断当前时间为整点时间，若当前时间是整点，则系统生成在0~59的0~5个随机数存放在redis/MySQL 中。
# 3、在main方法中，每次调度执行时，判断一下当前执行时间为第几分钟，看看是否包含在redis/MySQL中随机生成的数组中。若是包含则进行实际的接口调用，若是不包含则不执行真实的接口调用。
# 4、在MySQL中准备一张人口信息表（公民身份证号码）。
# 5、在调用接口时：身份证入参取人口信息表中随机进行提取，可使用分页查询的方式，每页一条，使用随机数（大小依数据量确定0~*）生成随机页。

# 定时任务schedule和多线程Timer(from threading import Timer)
import random
# 导入线程模块
import threading
import time
from os import *
import datetime
# 在python3中使用hashlib模块进行md5操作
import hashlib
import pymysql
import requests
import redis


# 获取连接对象conn;建立数据库的连接
def get_conn():
    conn = pymysql.connect(
        host="**.**.**.42",
        port=33086,
        user="sxyz_pxxy_web",
        passwd="pxxyweb*$DF&XJ",
        database='sxyz_pxxy_web'
    )
    return conn


# 查询
def select(sql):
    conn = get_conn()
    mycursor = conn.cursor()
    mycursor.execute(sql)
    results = mycursor.fetchall()
    conn.commit()
    mycursor.close()
    conn.close()
    for i in results:
        return (i[0])


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


def post_way(app_postsecret, sfz):
    appSecret = app_postsecret
    mkt = get_time_stamp13()
    str_md5 = appKey + appSecret + str(mkt)
    sign = md5(str_md5)
    data_dict = {
        "appKey": appKey,
        "sign": sign,
        "requestTime": mkt,
        "sfzh": sfz
    }
    url = "https://interface.zjzwfw.gov.cn/gateway/api/001003001/dataSharing/uU4lb0350783d2fa.htm?"
    headers = {}
    response = requests.post(url=url, headers=headers, data=data_dict)
    rep_obj = response.json()
    return rep_obj


def refresh_key():
    ref_dict = get_way("e011fbb67ccb441c93dc18e9b2f2d86b",
                       "http://interface.zjzwfw.gov.cn/gateway/app/refreshTokenByKey.htm?")
    print("ref")
    print(ref_dict)
    return ref_dict["datas"]['refreshSecret']


def request_key():
    ref_sec = refresh_key()
    req_dict = get_way(ref_sec, 'http://interface.zjzwfw.gov.cn/gateway/app/refreshTokenBySec.htm?')
    if (req_dict['code'] == "00"):
        # 将得到的密钥存入redis（rpush,从尾部取）
        r.rpush('req_list', req_dict["datas"]['requestSecret'])
        print("req")
        print(req_dict)
        return req_dict["datas"]['requestSecret']
    else:
        print('请求错误')


def JKM_search():
    # 数据表中随机读取身份证
    sql_page = "SELECT CEIL(COUNT(*) / 1000) FROM warehouse_people_focus"  # 获取总页码
    pageTotal = select(sql_page)
    # print('pageTotal    '+str(pageTotal))
    sql_count = "SELECT COUNT(*) FROM warehouse_people_focus"
    count = select(sql_count)
    # print('count    '+str(count))
    if (pageTotal == 1):
        offset = random.randint(0, count - 1)  # 闭区间
    else:
        last_pagecount = count - 1000 * (pageTotal - 1)
        offset = (random.randint(0, 1000) * random.randint(0, pageTotal - 1)) + random.randint(0, last_pagecount - 1)
    # print('offset   '+str(offset))
    sql_get = "SELECT id_card from warehouse_people_focus limit 1 OFFSET {}".format(offset)
    sfz = select(sql_get)
    # print('sfz  '+str(sfz))

    # 1、读取最新，2、校验分析是否失效，若是失效再进行调用上面步骤
    se_sec = r.lindex('req_list', -1).decode()
    # se_sec = "8aaf320622ef407f96e745fadb72eab1"
    se_check = post_way(se_sec, sfz)
    if (se_check['code'] == "00"):
        print(se_check)
    else:
        print("请求密钥失效,现重取")
        req = request_key()
        se_dict = post_way(req, sfz)
        print(se_dict)


def main():
    print("\033[0;32m%s\033[0m" % u"===================start===================")
    d1 = datetime.datetime.now()
    print(u"开始时间：", d1)
    # 初次运行，req_list里没有请求密钥；需要初始化
    if (r.lrange('req_list', 0, -1) == []):
        request_key()
    JKM_search()
    d2 = datetime.datetime.now()
    print(u"结束时间：", d2)
    print("\033[0;31m%s\033[0m" % u"总共耗时：", d2 - d1)
    print("\033[0;32m%s\033[0m" % u"===================stop===================")


# ---------------------------------------------------------------------------------------

def step2():
    # 2、判断当前时间为整点时间，若当前时间是整点，则系统生成在0~59的0~5个随机数存放在redis 中
    time_now = time.strftime('%H%M', time.localtime())
    # print(type(time_now))#<class 'str'>
    if int(time_now) >= 800 and int(time_now) <= 1900:
        # 如果时间在8:00~19:00,再判断是否是整点
        if int(time_now[-2:]) == 00:
            # 生成在0~59的0~5个随机数存放在redis 中
            ran_list = random.sample(range(0,60), random.randint(0,5))  # 生成0-5个随机数量的0-59的随机数存放在列表中
            if ran_list:
                for i in ran_list:
                    t = time_now[0:2]  # 取小时
                    if (len(str(i)) == 1):  # 若随机生成的数只有一位，则补0
                        i1 = '0' + str(i)
                        s = t + str(i1)
                        r.rpush('random_list', s)
                    else:
                        s = t + str(i)
                        r.rpush('random_list', s)
            else:
                print("随机生成的ran_list为空...")
            print(r.lrange('random_list', 0, -1))


def step3():
    # 3、每次调度执行时，判断一下当前执行时间为第几分钟，看看是否包含在redis / MySQL中随机生成的数组中。若是包含则进行实际的接口调用，若是不包含则不执行真实的接口调用。
    time_excute = time.strftime('%H%M', time.localtime())
    for i in r.lrange('random_list', 0, -1):
        if i.decode() == time_excute:  # 若是包含则进行实际的接口调用
            main()
            # 运行main函数调用健康码接口
        else:
            print("不执行接口调用-----")


def thread_Timer():
    print("使用调度函数-----")
    global timer  # 定义全局变量
    # 定时器构造函数主要有2个参数，第一个参数为时间，第二个参数为函数名
    timer = threading.Timer(60, thread_Timer)  # 60秒调用一次函数
    step2()
    step3()
    print("线程名称={}\n".format(timer.getName()))
    # 启用定时器
    timer.start()


if __name__ == "__main__":
    # 1、脚本启用定时调度，每分钟执行一次。
    # 创建并初始化线程
    t1 = threading.Timer(5, thread_Timer)
    # 启动线程
    t1.start()
    t1.start()
    print('定时器启动成功-----')