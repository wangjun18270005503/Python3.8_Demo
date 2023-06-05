# -*- coding: utf-8 -*- 
# @Project : Git_Python3.8_Demo 
# @Time : 2022/10/18 14:25 
# @Author : J.wang 
# @Version: V 0.1 
# @File : sdyl_js_szhgg_gjwsjkw_xgfy_hsjcsjfwjk.py
# @Software: PyCharm
# @desc : todo 模拟真实 刷调用量 浙江省共数据平台类型接口 数字化改革 国家卫生健康委_新冠肺炎_核酸检测数据服务接口
import redis, requests, pymysql, datetime
import json, random, hashlib
import time
import pandas as pd

pymysql.install_as_MySQLdb()
from sqlalchemy import create_engine

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


# todo (1)刷新密钥
def refresh_token_by_key(appKey, appSecret):
    print("开始《刷新密钥》")
    # 获取 sign
    key_sign = create_sign(appKey, appSecret)
    # 组合参数
    url = 'http://interface.zjzwfw.gov.cn/gateway/app/refreshTokenByKey.htm?'
    url = url + 'requestTime=' + requestTime + '&appKey=' + appKey + '&sign=' + key_sign
    response = requests.post(url)
    print(response.text)
    return response.json()['datas']['refreshSecret']


# todo (2)请求密钥
def refresh_token_by_sec(appKey, appSecret, key_name):
    print("开始《请求密钥》")
    # 获取 sign
    refreshSecret = refresh_token_by_key(appKey, appSecret)
    sec_sign = create_sign(appKey, refreshSecret)
    # 组合参数
    url = 'http://interface.zjzwfw.gov.cn/gateway/app/refreshTokenBySec.htm?'
    url = url + 'requestTime=' + requestTime + '&appKey=' + appKey + '&sign=' + sec_sign
    response = requests.post(url)
    requestSecret = response.json()['datas']['requestSecret']
    r.set(key_name + "_sign_zj", requestSecret)
    return requestSecret


# todo (3)业务接口
def gateway(url, appKey, appSecret, key_name):
    print("开始《业务接口》")
    # 获取 sign
    sign_r = create_sign(appKey, r.get(key_name + "_sign_zj"))
    # 获取随机 sfzh
    select_sql = "SELECT id_card AS zjhm,name AS xm FROM `js_population_info` WHERE del_flag = '0' LIMIT " + str(
        random.randint(1, 620000)) + ",1"
    db = create_engine(db_url)
    zjhm_df = pd.read_sql(select_sql, db)
    body_list = zjhm_df.to_dict('records')
    if len(body_list) != 0:
        body = body_list[0]
        # 组合参数
        url = url + 'requestTime=' + requestTime + '&appKey=' + appKey + '&sign=' + sign_r
        print(url)
        print(body)
        response = requests.post(url, data=body)
        print(response.text)
        if response.json()['code'] == '02' or response.json()['code'] == '11':
            refresh_token_by_sec(appKey, appSecret, key_name)


# todo (4)模拟真实
def Simulate_reality(url, appKey, appSecret, key_name):
    print('\033[0;34;40m 开始模拟真实生产平台人员请求 。。。 \033[0m')
    c_time = time.strftime("%H:%M:%S", time.localtime())  # 将本地时间转换为字符串，并格式化为 时：分：秒
    if c_time[3:5] == '00':  # 判断截取分钟是否为0
        # 若真想是准时的整时整分整秒，则放开此出
        # if c_time[6:8] == '00':  # 判断截取秒是否为0
        print('现在为整点:' + c_time)
        # 生成 随机运行时间点存放至 redis
        ran_list = random.sample(range(0, 59), random.randint(0, 20))
        ran_list = json.dumps(ran_list)
        print(ran_list)
        # 执行时间点存放至 redis
        r.set(key_name + "_minute_point_bp0550XeEUj4emea", ran_list)
    now_minute = time.strftime("%M", time.localtime())
    minute_list = json.loads(r.get(key_name + "_minute_point_bp0550XeEUj4emea"))
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

    url = 'https://interface.zjzwfw.gov.cn/gateway/api/001003001029/dataSharing/bp0550XeEUj4emea.htm?'
    appKey = 'A330881406627202107016701'
    appSecret = 'e011fbb67ccb441c93dc18e9b2f2d86b'
    key_name = 'szhgg'
    # todo 2 启动调用程序
    Simulate_reality(url, appKey, appSecret, key_name)
    # refresh_token_by_sec(appKey, appSecret, key_name)
    # todo 3 程序结束时间 并输出总耗时
    endTime = datetime.datetime.now()
    durTime = '\033[0;33;40m funtion time use:%dms \033[0m' % (
            (endTime - startTime).seconds * 1000 + (endTime - startTime).microseconds / 1000)
    print(durTime)
