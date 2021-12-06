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
import pymysql
import requests,time,redis,hashlib
requestTime = str(int(time.time()*1000))
print('当前请求时间戳（毫秒）：'+requestTime)


def ApiBatchRetained(url,appKey,appSecret,loop_table_name,create_name,*params):
    print('url：'+url+'\nappKey：'+appKey+'\nloop_table_name'+loop_table_name+'\ncreate_name'+create_name)
    params1 = ''
    for param in range(len(params)):
        print(params[param])
        params1 += ','
        params1 += params[param]
        print()
    try:
        db = pymysql.Connect(host='10.27.166.210', user='xxzhcs', password='Xxzhcs1234', port=3306,
                             database='sx_data_share')
        # 使用cursor()方法获取操作游标
        govtest_cursor = db.cursor()
        select_loop_info = "SELECT " + params[param] + " FROM " + loop_table_name + " where del_flag = '0';"
        # 执行SQL语句
        govtest_cursor.execute(select_loop_info)
        # 返回查询结果
        data1 = govtest_cursor.fetchall()
        print(data1)
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
    appSecret = '31b4020cd1c6419bb48bd27e6b239282'
    loop_table_name = 'loop_handicapped'
    create_name = '000000000000000022'
    param = 'cardId'
    ApiBatchRetained(url,appKey,appSecret,loop_table_name,create_name,param)