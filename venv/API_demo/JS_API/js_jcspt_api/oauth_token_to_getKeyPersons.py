# -*- coding: utf-8 -*- 
# @Project ：Git_Python3.8_Demo 
# @Time : 2021/12/27 16:36 
# @Author : J.wang 
# @Version：V 0.1 
# @File : oauth_token_to_getKeyPersons.py
# @Software: PyCharm
# @desc :  生产——获取重点人员巡查记录列表
import pymysql,requests
import redis

appkey = 'MBMAWSCLUWYWBAAKMQEH'
username = 'Azdry01@qzsg'
password = 'afdd0b4ad2ec172c586e2150770fbf9e'
# 连接redis:
r = redis.Redis(host='10.50.207.215', port=6379, db=6, password='sx123456', decode_responses=True)
auth = r['access_token']
print('\033[5;35;40m\t当前登录验证token \033[0m：', auth)

# 登录接口
token_url = "http://gateway.daliandong.cn/api/jczl_prod_quzhou/oauth/token.json"
# post 请求参数 存放于 Body  x-www-form-urlencoded
token_body_data = {'appKey': "MBMAWSCLUWYWBAAKMQEH",
                   'bizContent': "{'username':'" + username + "','password':'" + password + "','grant_type':'password','scope':'all','Authorization':'Basic dXNlcmNlbnRlcjoxMTg2MDQ1ZDU1OTlkZTZlZjJjYTI4MjM0N2E1NWNhMg=='}"}
print('登录接口请求参数组装：', token_body_data)

# 巡查记录详情 业务接口调用
record_info_url = 'http://gateway.daliandong.cn/api/jczl_prod_quzhou/patrol/getRecordById.json'
# 组装参数：
# # 请求头
record_info_headers = {'auth': auth}
print('请求头设置：', record_info_headers)
# 查询循环表
try:
    db = pymysql.Connect(host='127.0.0.1', user='root', password='159611', port=3306, database='python_mysql')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    select_loop_info = "SELECT info_id FROM loop_recordinfo_id where del_flag = '0';"
    print(select_loop_info)
    # 执行SQL语句
    cursor.execute(select_loop_info)
    # 返回查询结果
    param_list = cursor.fetchmany(10000)  # 指定循环次数
    # 组合body请求参数
    for i in range(len(param_list)):
        record_info_body = {'appKey': "MBMAWSCLUWYWBAAKMQEH", 'bizContent': "{'id':'"+param_list[i][0]+"'}"}
        print('请求体：', record_info_body)
        # 发送请求
        record_info_respose = requests.post(record_info_url, data=record_info_body, headers=record_info_headers)
        print('巡查记录返回数据：',record_info_respose.text)

except pymysql.Error as e:
    print("数据库连接失败：" + str(e))
finally:
    if db:
        db.close()
        print('关闭数据库连接....')

# 发送登录请求
# respose = requests.post(token_url, data=token_body_data)
# r.set('access_token', respose.json()['access_token'])  # 将登录密钥存放至redis 中便于后续接口调用
