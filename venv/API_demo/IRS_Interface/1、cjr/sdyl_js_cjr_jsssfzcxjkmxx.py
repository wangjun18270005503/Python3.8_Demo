# -*- coding: utf-8 -*- 
# @Project : Git_Python3.8_Demo 
# @Time : 2022/10/17 17:13 
# @Author : J.wang 
# @Version: V 0.1 
# @File : sdyl_js_cjr_jsssfzcxjkmxx.py
# @Software: PyCharm
# @desc : todo 模拟真实 刷调用量 江山公共数据平台类型接口 残疾人项目 江山市身份证查询健康码信息
'''
实现思路：
 1、脚本启用定时调度，每分钟执行一次。
 2、在main方法中，每次执行时判断当前时间为整点时间，若当前时间是整点，则系统生成在0~59的0~10个随机数存放在redis/MySQL 中。
 3、在main方法中，每次调度执行时，判断一下当前执行时间为第几分钟，看看是否包含在redis/MySQL中随机生成的数组中。若是包含则进行实际的接口调用，若是不包含则不执行真实的接口调用。
 4、在MySQL中准备一张人口信息表（公民身份证号码）。
 5、在调用接口时：身份证入参取人口信息表中随机进行提取，可使用分页查询的方式，每页一条，使用随机数（大小依数据量确定0~*）生成随机页。
'''

import redis, requests, pymysql, datetime
import json, random, hashlib
import time
import pandas as pd

requests.packages.urllib3.disable_warnings()
pymysql.install_as_MySQLdb()
from sqlalchemy import create_engine

# 连接 redis
r = redis.Redis(host='10.27.235.199', port=9004, db=15, password='sx123456', decode_responses=True)
requestTime = str(int(time.time() * 1000))
# 公共资源
db_url = 'mysql://jsggsj:M^*fgp&x@10.27.170.42:33086/xxzhcs?charset=utf8'


# todo sign 前面生成
def create_sign(ak, sk):
    print('开始生成 sign')
    str = ak + sk + requestTime
    sign = hashlib.md5()
    sign.update(str.encode("utf-8"))
    return sign.hexdigest()


# todo (1)刷新密钥
def refresh_token_by_key(appKey, appSecret):
    print("开始《刷新密钥》")
    # 组合参数
    url = 'http://szgg.jiangshan.gov.cn:81/appsecert'
    data = {"appKey": appKey,
            "appSecret": appSecret}
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(response.text)
    return response.json()


# todo (2)请求密钥
def refresh_token_by_sec(appKey, appSecret, key_name):
    print("开始《请求密钥》")
    # 获取 sign
    res = refresh_token_by_key(appKey, appSecret)
    refreshSecret = res['data']['refreshSecret']
    requestTime = res['data']['requestTime']
    # 组合参数
    url = 'http://szgg.jiangshan.gov.cn:81/interfaceSecurity'

    data = {"appKey": appKey,
            "refreshSecret": refreshSecret,
            "requestTime": requestTime}
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    requestSecret = response.json()['data']['requestSecret']
    r.set(key_name + "_sign_js", requestSecret)
    return requestSecret


# todo (3)业务接口
def gateway(url, appKey, appSecret, key_name):
    print("开始《业务接口》")
    # 获取 sign
    sign_r = create_sign(appKey, r.get(key_name + "_sign_js"))
    # 获取随机 sfzh
    select_sql = "SELECT id_card FROM `js_population_info` LIMIT " + str(random.randint(1, 620000)) + ",1"
    db = create_engine(db_url)
    sfzh_df = pd.read_sql(select_sql, db)
    sfzh_list = sfzh_df['id_card'].to_list()
    if len(sfzh_list) != 0:
        data = {"sfzh": sfzh_list[0]}
        print(data)
        # 组合参数
        url = url + 'requestTime=' + requestTime + '&appkey=' + appKey + '&sign=' + sign_r

        print(url)
        response = requests.post(url, data=json.dumps(data), verify=False)
        print(response.text)
        if response.status_code != 200:
            if response.json()['rtnCode'] == 401 or response.json()['rtnCode'] == 11:
                refresh_token_by_sec(appKey, appSecret, key_name)


# todo (4)模拟真实
def Simulate_reality(url, appKey, appSecret, key_name):
    print('\033[0;34;40m 开始模拟真实生产平台人员请求 。。。 \033[0m')
    c_time = time.strftime("%H:%M:%S", time.localtime())  # 将本地时间转换为字符串，并格式化为 时：分：秒
    if c_time[3:5] == '00':  # 判断截取分钟是否为0
        # if c_time[6:8] == '00':  # 判断截取秒是否为0
        print('现在为整点:' + c_time)
        # 生成 随机运行时间点存放至 redis
        ran_list = random.sample(range(0, 59), random.randint(0, 20))
        ran_list = json.dumps(ran_list)
        print(ran_list)
        # 执行时间点存放至 redis
        r.set(key_name + "_minute_point_J2eVaMeid482W6F8", ran_list)
    now_minute = time.strftime("%M", time.localtime())
    minute_list = json.loads(r.get(key_name + "_minute_point_J2eVaMeid482W6F8"))
    print(minute_list)
    # 判别当前时间与
    for i in iter(minute_list):
        if i == int(now_minute):
            # 发送请求
            gateway(url, appKey, appSecret, key_name)


if __name__ == '__main__':
    # todo 1 程序开始时间
    startTime = datetime.datetime.now()
    print('\033[0;33;40m Program starts running 。。。 \033[0m')

    url = 'https://10.27.168.100:9443/J2eVaMeid482W6F8/bp?'
    appKey = 'KeLJJ9hyj2e6eQwtIxHp'
    appSecret = 'rPStGHZpmGh9Ah8uMZ8V'
    key_name = 'cjr'
    # todo 2 启动调用程序
    Simulate_reality(url, appKey, appSecret, key_name)
    # refresh_token_by_sec(appKey, appSecret, key_name)
    # todo 3 程序结束时间 并输出总耗时
    endTime = datetime.datetime.now()
    durTime = '\033[0;33;40m funtion time use:%dms \033[0m' % (
            (endTime - startTime).seconds * 1000 + (endTime - startTime).microseconds / 1000)
    print(durTime)
