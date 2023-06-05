#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/12/6 16:22
# @Author : J.wang
# @Version：V 0.1
# @File : qz_ApiBatchRetained.py
# @desc : （3) 省市公共数据平台_批量数据留存
'''
    通过 XXL—JOB: 传参
    url：接口地址
    appKey：应用key
    appSecret：应用appSecret
    params：param1、param2 接口循环入参参数英文名称
    loop_table_name：loop循环表
    create_name：需要创建对应的表名称
'''
import pymysql, json
import requests, time, redis, hashlib

requestTime = str(int(time.time() * 1000))
print('当前请求时间戳（毫秒）：' + requestTime)
# 连接 redis
r = redis.Redis(host='localhost', port=6379, db=1, decode_responses=True)


# MD5 数据加工
def str_md5(str=''):
    md = hashlib.md5()
    md.update(str.encode(encoding="utf-8"))
    return md.hexdigest()


def create_table():
    print('开始自动建表！！！')


# 定义方法传参形式
def gateway(url, appKey, appSecret, key_value):
    # 打印参数信息
    print('url：' + url + '\nappKey：' + appKey + '\nappSecret：' + appSecret)
    # todo 准备参数
    # (1) appKey  (参数自带)
    # (2) requestTime （获取当前时间戳）
    # (3) sign
    str = appKey + appSecret + requestTime
    sign = str_md5(str)
    # (4) 业务参数  (查询接口配置信息)
    # 组合参数
    params = {"appKey": appKey, "sign": sign, "requestTime": requestTime}
    print(type(params))
    print(type(key_value))
    param_dict = params.update(key_value)
    print('*********************')
    print(params)
    print('*********************')
    response = requests.get(url, params).json()
    print(response)
    print(type(response))
    # if response != None and response['code'] == '00':
    # 存储数据


def ApiBatchRetained(url, appKey, appSecret, loop_table_name, create_name, *params):
    print('url：' + url + '\nappKey：' + appKey + '\nloop_table_name：' + loop_table_name + '\ncreate_name：' + create_name)
    param = ",".join(str(params[n]) for n in range(len(params)))
    print('param：' + param)
    try:
        db = pymysql.Connect(host='**.**.**.210', user='x*z*x*', password='X*z*c*1234', port=3306,
                             database='sx_data_share')
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        select_loop_info = "SELECT " + param + " FROM " + loop_table_name + " where del_flag = '0';"
        # 执行SQL语句
        cursor.execute(select_loop_info)
        # 返回查询结果
        param_list = cursor.fetchmany(10)
        # param_list = (('34260119851110502X', '谈金云'), ('330823197304095114', '周良君'), ('330881201209195523', '周心宜'), ('330823197204154113', '周明水'), ('330823197508244142', '严雪荣'), ('330881200204184118', '周鹏辉'), ('33088119990615572X', '毛青霞'), ('330823197102014929', '周杨芳'), ('330881199708243921', '周婷'), ('330881200102277532', '毛威军'))
        # param_list = cursor.fetchall()
        print(param_list)
        # 传参、调用接口
        for i in range(len(param_list)):
            param_str = '{' + ",".join(
                '"' + str(params[n] + '":"' + str(param_list[i][n]) + '"') for n in range(len(params))) + '}'
            gateway(url, appKey, appSecret, eval(param_str))
    except pymysql.Error as e:
        print("数据库连接失败：" + str(e))
    finally:
        if db:
            db.close()
            print('关闭数据库连接....')


# 调用方法 刷新请求密钥方法
if __name__ == "__main__":
    url = 'https://dw.qz.gov.cn/gateway/api/001008013008001/dataSharing/p6b45bR28ejPr6z3.htm?'
    appKey = '46eb7734001641048cd20cf15f18610a'
    appSecret = r['requestSecret']
    loop_table_name = 'loop_handicapped'
    create_name = '000000000000000022'
    param = 'cardId'
    param2 = 'name'
    ApiBatchRetained(url, appKey, appSecret, loop_table_name, create_name, param, param2)
