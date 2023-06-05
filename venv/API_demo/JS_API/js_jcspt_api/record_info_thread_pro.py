# -*- coding: utf-8 -*- 
# @Project ：Git_Python3.8_Demo 
# @Time : 2021/12/29 14:17 
# @Author : J.wang 
# @Version：V 0.1 
# @File : record_info_thread_pro.py
# @Software: PyCharm
# @desc :  生产 启用线程池调用 政法委基层治理四平台重点人员巡查走访详情接口 留存数据

from concurrent.futures import ThreadPoolExecutor
import threading
import re
import pymysql, json, math, random
import requests, time, redis, hashlib

requestTime = str(int(time.time() * 1000))
print('当前请求时间戳（毫秒）：' + requestTime)
# 连接redis:
r = redis.Redis(host='10.50.207.215', port=6379, db=6, password='sx1~&~6', decode_responses=True)


def split_list(valuesList, keyslist):
    # 线程列表
    new_value_list = []
    count_list = []
    keys_list = []
    # 每个线程处理的数据大小
    split_count = 1
    # 需要的线程个数
    times = math.ceil(len(valuesList) / split_count)
    count = 0
    for item in range(times):
        keys_list.append(keyslist)
        value_list = valuesList[count: count + split_count]
        # print('\033[0;34;43m--待循环参数 value_list：--\033[0m', value_list, type(value_list))
        new_value_list.append(value_list)
        count_list.append(count)
        print('---------------------', count_list)
        count += split_count
    return new_value_list, count_list, keys_list


def work1(new_list, count_list, keyslist):
    sleep_time = random.randint(1, 1)  # 1~2 的随机沉睡时间
    print('\033[0;33;40m\t1~5 的随机沉睡时间，当前为：\033[0m', sleep_time)
    print(f'当前获取列表的数据为： {new_list},线程名称：{threading.current_thread().name}')
    # print(f'当前获取列表的数据为： {df},\t沉睡时间： {sleep_time},list is {_list},线程名称：{threading.current_thread().name}')
    # time.sleep(sleep_time)
    print('\033[0;34;40m--待循环参数 new_list：--\033[0m', new_list, '\033[0;34;40m--count_list：--\033[0m', count_list)
    try:
        keyslist1 = tuple(keyslist)[0]
        print('\033[0;34;40m--待循环参数 取第一位数据 keyslist_1：--\033[0m', keyslist1)
        param_str = '{' + ",".join(
            '"' + str(keyslist1[n] + '":"' + str(new_list[0][n]) + '"') for n in range(len(keyslist1))) + '}'
        print('\033[0;34;40m--param_str：--\033[0m', param_str)
        gateway(url, appkey, username, password, eval(param_str), create_name, table_comment)
    except Exception as e:
        print(e)
        pass
    return sleep_time, new_list, count_list


def threadPool_new(valuesList, keyslist):
    with ThreadPoolExecutor(max_workers=pool_num) as pool:
        print('\033[0;34;40m--待循环参数 keyslist：--\033[0m', keyslist, '\033[0;34;40m--待循环参数 valuesList：--\033[0m',
              valuesList)
        new_list, count_list, keys_list = split_list(valuesList, keyslist)

        # 使用map的优点是 每次调用回调函数的结果不用手动的放入结果list中
        results = pool.map(work1, new_list, count_list, keys_list)
        print(type(results))
        print('thread execute end!')


# （1）登录接口 token
def refreshTokenByKey(appKey, username, password):
    # 登录接口
    token_url = "http://gateway.daliandong.cn/api/jczl_prod_quzhou/oauth/token.json"

    # post 请求参数 存放于 Body  x-www-form-urlencoded
    token_body_data = {'appKey': "MBMAWSCLUWYWBAAKMQEH",
                       'bizContent': "{'username':'" + username + "','password':'" + password + "','grant_type':'password','scope':'all','Authorization':'Basic dXNlcmNlbnRlcjoxMTg2MDQ1ZDU1OTlkZTZlZjJjYTI4MjM0N2E1NWNhMg=='}"}
    response = requests.post(token_url, data=token_body_data).json()
    if response != None and response['code'] == 200:
        print('\033[5;30;46m\t（1）生产用户登录接口 返回参会参数：\033[0m', response)
        # 存储至redis
        # r = redis.Redis(host='localhost', port=6379, db=1, decode_responses=True)
        r.set('access_token', response['access_token'])  # 设置 name 对应的值


# 解析json存储数据
def insert_into_info(response):
    try:
        # 数据库链接
        govdb = pymysql.Connect(host='127.0.0.1', user='root', password='159611', port=3306, database='python_mysql')
        # 使用cursor()方法获取操作游标
        govtest_cursor = govdb.cursor()
        print(response['data'])
        # 调用接口
        # message = response.text
        # print message
        # 解析接口
        # pt = json.loads(message)
        # 所属区域
        checkOrgName = response['data']['checkOrgName']
        # 备注、检查地址
        visitRecord = response['data']['visitRecord']

        # 检查结果
        rcqjqk = ""
        gzqk = ""
        wlryqk = ""
        sxdt = ""
        llfy = ""

        # 获取检查情况
        for i in response['data']['checkPointRecordVOs']:
            # print i['checkPointRecord']['visitRecordId'],i['checkPointRecord']['checkPointName'],i['checkPointRecord']['passResult']

            if (i['checkPointRecord']['checkPointName'] == "日常起居情况"):
                rcqjqk = i['checkPointRecord']['passResult']
            elif (i['checkPointRecord']['checkPointName'] == "工作情况"):
                gzqk = i['checkPointRecord']['passResult']
            elif (i['checkPointRecord']['checkPointName'] == "往来人员情况"):
                wlryqk = i['checkPointRecord']['passResult']
            elif (i['checkPointRecord']['checkPointName'] == "思想动态"):
                sxdt = i['checkPointRecord']['passResult']
            elif (i['checkPointRecord']['checkPointName'] == "邻里反映"):
                llfy = i['checkPointRecord']['passResult']

        # 获取附件信息
        for i2 in response['data']['remarkFiles']:
            if (i['checkPointRecord']['visitRecordId'] == i2['visitRecordId']):
                fjxx = i2['visitRecordId']
            # 插入数据表
            insertsql = "insert into local_tqxtdj_xcjlxq(businessName,cardId,address,id,rcqjqk,gzqk,wlryqk,sxdt,llfy,checkAddress,remark,\
                                         visitRecordId,internalUrl,checkOrgName,checkUserName,peerChecker,checkDate) values \
                                        ('%s', '%s', '%s','%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
                        (visitRecord['businessName'], visitRecord['cardId'], visitRecord['address'],
                         i['checkPointRecord']['visitRecordId'], rcqjqk, gzqk, wlryqk, sxdt, llfy,
                         visitRecord['checkAddress'], visitRecord['remark'], fjxx, i2['downloadFileVO']['internalUrl'],
                         checkOrgName, visitRecord['checkUserName'], visitRecord['peerChecker'],
                         visitRecord['checkDate'])
        # 执行SQL
        govtest_cursor.execute(insertsql)
        # 提交
        govdb.commit()
    except pymysql.Error as e:
        print("数据库连接失败：" + str(e))
    finally:
        if govdb:
            govdb.close()
            print('关闭数据库连接....')


# 定义方法传参形式
def gateway(url, appKey, username, password, key_value, create_name, table_comment):
    # todo 准备参数
    # # 请求头
    auth = r['access_token']
    record_info_headers = {'auth': auth}
    print('++++++++++请求参数id++++++++++', key_value)

    # (4) 业务参数  (查询接口配置信息)
    # 组合参数
    params = {'appKey': "MBMAWSCLUWYWBAAKMQEH", 'bizContent': str(key_value)}
    # param_dict = params.update(key_value)
    print('\033[0;33;40m请求参数：\033[0m', params)
    response = requests.post(url, data=params, headers=record_info_headers).json()
    print('\033[5;30;46m\t接口返回参会参数：\033[0m', response)

    if response != None and response['success']:
        # 存储数据
        print('\033[0;33;40m\t开始插入数据：\033[0m')
        # fordata(create_name, table_comment, response)
        insert_into_info(response)
        print('插入数据：', response)
    else:
        print('签名错误')
        refreshTokenByKey(appKey, username, password)


def ApiBatchRetained_select(url, appKey, username, password, loop_table_name, create_name, table_comment, pool_num,
                            *params):
    print('url：' + url + '\nappKey：' + appKey + '\nloop_table_name：' + loop_table_name + '\ncreate_name：' + create_name)
    param = ",".join(str(params[n]) for n in range(len(params)))
    print('param：' + param)
    try:
        db = pymysql.Connect(host='127.0.0.1', user='root', password='159611', port=3306,
                             database='python_mysql')
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        select_loop_info = "SELECT " + param + " FROM " + loop_table_name + " where del_flag = '0';"
        print(select_loop_info)
        # 执行SQL语句
        cursor.execute(select_loop_info)
        # 返回查询结果
        param_list = cursor.fetchmany(10)  # 指定循环次数
        # param_list = cursor.fetchall()
        print('\033[0;34;40m--待循环参数：--\033[0m', param_list)
        print('params++++++++', params)
        # 尝试使用 多线程 请求接口
        params_key_list = []
        params_key_list.append(params)
        # 需要处理的数据
        keysDict = []
        keysDict.append(params)

        threadPool_new(list(param_list), list(keysDict))
    except pymysql.Error as e:
        print("数据库连接失败：" + str(e))
    finally:
        # if db:
        #     db.close()
        print('关闭数据库连接....')


# 调用方法 刷新请求密钥方法
if __name__ == "__main__":
    print('startTiem', str(int(time.time() * 1000)))
    # 业务接口地址
    url = 'http://gateway.daliandong.cn/api/jczl_prod_quzhou/patrol/getRecordById.json'
    appkey = 'MBMAWSCLUWYWBAAKMQEH'
    username = 'Azdry01@qzsg'
    password = 'afdd0b4ad2ec172c586e2150770fbf9e'
    loop_table_name = 'local_tqxtdj_fyjlcx'
    create_name = 'local_tqxtdj_info'
    table_comment = '政法委基层四平台巡查记录详情'
    pool_num = 5  # 线程数
    param = 'id'
    # param2 = 'name'
    ApiBatchRetained_select(url, appkey, username, password, loop_table_name, create_name, table_comment, pool_num,
                            param)
    # refreshTokenByKey(appkey, username, password)
    print('endTiem', str(int(time.time() * 1000)))
