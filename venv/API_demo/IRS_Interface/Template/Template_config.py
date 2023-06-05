# -*- coding: utf-8 -*- 
# @Project : Git_Python3.8_Demo 
# @Time : 2022/10/18 17:21 
# @Author : J.wang 
# @Version: V 0.1 
# @File : Template_config.py
# @Software: PyCharm
# @desc : 配置版 刷调用量
'''
（1）、经过分析由于申请的接口调用方式，入参形式、各层级签名类似，为避免大量重复代码工作。
（2）、将调用接口所需的 Ak、SK、接口url、入参封装、sign组名定义、接口分钟组名定义、签名异常校验code 等相关信息已配置形式配置
（3）、配置存放至 **.**.**.42中的x*z*x*数据库的 sys_sdyl_js_projtect_config：江山市IRS应用接口刷调用量_配置表 下面
（4）、解析江山市IRS应用接口刷调用量_配置表中的配置信息，实现封装随机接口调用形式。
'''

import redis, requests, pymysql, datetime
import json, random, hashlib
import time
import pandas as pd

requests.packages.urllib3.disable_warnings()
pymysql.install_as_MySQLdb()
from sqlalchemy import create_engine, text

# 连接 redis
r = redis.Redis(host='**.**.*35.199', port=9004, db=15, password='sx1~&~6', decode_responses=True)
requestTime = str(int(time.time() * 1000))
# 公共资源
db_url = 'mysql://**:**@**.**.**.42:****/x*z*x*?charset=utf8'


# todo sign 前面生成
def create_sign(ak, sk):
    print('开始生成 sign')
    str = ak + sk + requestTime
    sign = hashlib.md5()
    sign.update(str.encode("utf-8"))
    return sign.hexdigest()


# todo 省 (1)刷新密钥
def refresh_token_by_key_zj(config_dict):
    print("开始《浙江省——刷新密钥》")
    # 获取 sign
    key_sign = create_sign(config_dict['app_key'], config_dict['app_secret'])
    # 组合参数
    url = 'http://interface.zjzwfw.gov.cn/gateway/app/refreshTokenByKey.htm?'
    url = url + 'requestTime=' + requestTime + '&appKey=' + config_dict['app_key'] + '&sign=' + key_sign
    response = requests.post(url)
    print(response.text)
    return response.json()['datas']['refreshSecret']


def refresh_token_by_key_qz(config_dict):
    print("开始《衢州市——刷新密钥》")
    # 获取 sign
    key_sign = create_sign(config_dict['app_key'], config_dict['app_secret'])
    # 组合参数
    url = 'http://dw.qz.gov.cn/gateway/app/refreshTokenByKey.htm?'
    url = url + 'requestTime=' + requestTime + '&appKey=' + config_dict['app_key'] + '&sign=' + key_sign
    response = requests.post(url)
    print(response.text)
    return response.json()['datas']['refreshSecret']


def refresh_token_by_key_js(config_dict):
    print("开始《江山市——刷新密钥》")
    # 组合参数
    url = 'http://szgg.jiangshan.gov.cn:81/appsecert'
    data = {"appKey": config_dict['app_key'],
            "appSecret": config_dict['app_secret']}
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(response.text)
    return response.json()


# ******************************************************************************************************

# todo 省 (2)请求密钥
def refresh_token_by_sec_zj(config_dict):
    print("开始《浙江省——请求密钥》")
    # 获取 sign
    refreshSecret = refresh_token_by_key_zj(config_dict)
    sec_sign = create_sign(config_dict['app_key'], refreshSecret)
    # 组合参数
    url = 'http://interface.zjzwfw.gov.cn/gateway/app/refreshTokenBySec.htm?'
    url = url + 'requestTime=' + requestTime + '&appKey=' + config_dict['app_key'] + '&sign=' + sec_sign
    response = requests.post(url)
    requestSecret = response.json()['datas']['requestSecret']
    r.set(config_dict['sing_name'] + "_sign_" + config_dict['interface_level'], requestSecret)
    return requestSecret


def refresh_token_by_sec_qz(config_dict):
    print("开始《衢州市——请求密钥》")
    # 获取 sign
    refreshSecret = refresh_token_by_key_qz(config_dict)
    sec_sign = create_sign(config_dict['app_key'], refreshSecret)
    # 组合参数
    url = 'http://dw.qz.gov.cn/gateway/app/refreshTokenBySec.htm?'
    url = url + 'requestTime=' + requestTime + '&appKey=' + config_dict['app_key'] + '&sign=' + sec_sign
    response = requests.post(url)
    requestSecret = response.json()['datas']['requestSecret']
    r.set(config_dict['sing_name'] + "_sign_" + config_dict['interface_level'], requestSecret)
    return requestSecret


def refresh_token_by_sec_js(config_dict):
    print("开始《江山市——请求密钥》")
    # 获取 sign
    res = refresh_token_by_key_js(config_dict)
    refreshSecret = res['data']['refreshSecret']
    requestTime = res['data']['requestTime']
    # 组合参数
    url = 'http://szgg.jiangshan.gov.cn:81/interfaceSecurity'

    data = {"appKey": config_dict['app_key'],
            "refreshSecret": refreshSecret,
            "requestTime": requestTime}
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    requestSecret = response.json()['data']['requestSecret']
    r.set(config_dict['sing_name'] + "_sign_" + config_dict['interface_level'], requestSecret)
    return requestSecret


# todo (3)业务接口
# def gateway(url, appKey, appSecret, key_name):
def gateway(config_dict):
    print("开始《业务接口》")
    # 获取 sign
    sign_r = create_sign(config_dict['app_key'],
                         r.get(config_dict['sing_name'] + "_sign_" + config_dict['interface_level']))
    db = create_engine(db_url)
    # 省市 适配 区县 参数
    appk_name = ''
    if config_dict['interface_level'] == 'js':
        appk_name = '&appkey='
    else:
        appk_name = '&appKey='
    url = config_dict['interface_url'] + 'requestTime=' + requestTime + appk_name + config_dict[
        'app_key'] + '&sign=' + sign_r
    body_df = pd.read_sql(text(config_dict['select_sql']), db)
    # 写入日志 表
    insert_pd = pd.DataFrame(
        columns=['project_name', 'app_key', 'app_secret', 'interface_name', 'interface_level','request_mode', 'res_info', 'req_info'],
        index=["0"])
    insert_pd['project_name'] = config_dict['project_name']
    insert_pd['app_key'] = config_dict['app_key']
    insert_pd['app_secret'] = config_dict['app_secret']
    insert_pd['interface_name'] = config_dict['interface_name']
    insert_pd['interface_level'] = config_dict['interface_level']
    insert_pd['request_mode'] = config_dict['request_mode']

    if config_dict['request_mode'] == 'GET':
        print("GET")
        params = ''
        columns = body_df.columns
        body_list = body_df.values[0]
        for i in range(len(body_list)):
            params = params + '&' + columns[i] + '=' + body_list[i]
        url = url + params
        print(url)
        response = requests.get(url)
        insert_pd['req_info'] = url
    else:
        body_list = body_df.to_dict('records')
        if len(body_list) != 0:
            body = body_list[0]
        print(body)
        print(url)
        body = json.dumps(body)
        response = requests.post(url, data=body, verify=False)
        insert_pd['req_info'] = body

    insert_pd['res_info'] = response.text
    insert_pd.to_sql('sys_sdyl_js_projtect_log', con=db, if_exists='append', index=False)
    print(insert_pd)
    print(response.text)

    if '秘钥' in response.text or response.status_code != 200:
        if config_dict['interface_level'] == 'zj':
            refresh_token_by_sec_zj(config_dict)
        if config_dict['interface_level'] == 'qz':
            refresh_token_by_sec_qz(config_dict)
        if config_dict['interface_level'] == 'js':
            refresh_token_by_sec_js(config_dict)


# todo (4)模拟真实
def Simulate_reality(config_dict):
    minute_name = config_dict['minute_name']
    print('\033[0;34;40m 开始模拟真实生产平台人员请求 。。。 \033[0m')
    c_time = time.strftime("%H:%M:%S", time.localtime())  # 将本地时间转换为字符串，并格式化为 时：分：秒
    if c_time[3:5] == '00':  # 判断截取分钟是否为0
        # 若真想是准时的整时整分整秒，则放开此出
        # if c_time[6:8] == '00':  # 判断截取秒是否为0
        print('现在为整点:' + c_time)
        # 生成 随机运行时间点存放至 redis
        ran_list = random.sample(range(0, 59), random.randint(int(config_dict['random_start_num']),
                                                              int(config_dict['random_end_num'])))
        ran_list = json.dumps(ran_list)
        print(ran_list)
        # 执行时间点存放至 redis
        r.set(config_dict['sing_name'] + "_minute_point_" + config_dict['minute_name'], ran_list)
    now_minute = time.strftime("%M", time.localtime())
    minute_list = json.loads(r.get(config_dict['sing_name'] + "_minute_point_" + config_dict['minute_name']))
    print(minute_list)
    # 判别当前时间与
    for i in iter(minute_list):
        if i == int(now_minute):
            # 发送请求
            gateway(config_dict)


# 获取配置详情
def get_config_info():
    sql_str = "SELECT project_name,app_key,app_secret,interface_name,interface_url,interface_level,select_sql,sing_name,minute_name,res_code,request_mode,random_start_num,random_end_num FROM `sys_sdyl_js_projtect_config` WHERE del_flag = 0 AND task_code = '2';"
    db = create_engine(db_url)
    config_list = pd.read_sql(sql_str, db)
    config_dict_list = config_list.to_dict('records')
    if len(config_dict_list) != 0:
        for config_dict in iter(config_dict_list):
            print(config_dict)
            Simulate_reality(config_dict)
            # if config_dict['interface_level'] == 'zj':
            #     refresh_token_by_sec_zj(config_dict)
            # if config_dict['interface_level'] == 'qz':
            #     refresh_token_by_sec_qz(config_dict)
            # if config_dict['interface_level'] == 'js':
            #     refresh_token_by_sec_js(config_dict)


if __name__ == '__main__':
    # todo 1 程序开始时间
    startTime = datetime.datetime.now()
    print('\033[0;33;40m Program starts running 。。。 \033[0m')

    # todo 2 启动调用程序
    get_config_info()
    # todo 3 程序结束时间 并输出总耗时
    endTime = datetime.datetime.now()
    durTime = '\033[0;33;40m funtion time use:%dms \033[0m' % (
            (endTime - startTime).seconds * 1000 + (endTime - startTime).microseconds / 1000)
    print(durTime)
