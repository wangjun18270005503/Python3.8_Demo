import requests, json, datetime, hashlib
import time, redis, schedule, random
from sqlalchemy import create_engine

time_stamp = str(int(time.time() * 1000))
# 连接redis
r = redis.Redis(host='127.0.0.1',port=6379,db=0)

# 连接mysql
db = create_engine('mysql+mysqldb://sxyz_pxxy_web:pxxyweb*$DF&XJ@**.**.**.42:****/sxyz_pxxy_web?charset=utf8')


#sign 签名
def md5value(appKey,appSecret):

    str = appKey + appSecret + time_stamp
    sign = hashlib.md5()
    sign.update(str.encode("utf-8"))
    sign = sign.hexdigest()
    return sign


# 刷新密钥
def get_refresh(appKey,sign):
    url = 'http://interface.zjzwfw.gov.cn/gateway/app/refreshTokenByKey.htm'
    params = {
        'appKey':appKey,
        'sign':sign,
        'requestTime':time_stamp
    }
    response = requests.get(url,params)
    if response.status_code == 200:
        response = response.json()
        refreshSecret = response['datas']['refreshSecret']
        print("接口请求结束--------------------------------------------------")
        return refreshSecret
    else:
        print("接口请求失败--------------------------------------------------")


# 请求密钥
def get_secret(appKey,sign):
    url = 'http://interface.zjzwfw.gov.cn/gateway/app/refreshTokenBySec.htm'
    params = {
        'appKey': appKey,
        'sign': sign,
        'requestTime': time_stamp
    }
    response = requests.get(url,params)
    if response.status_code == 200:
        response = response.json()
        requestSecret = response['datas']['requestSecret']

        print("接口请求结束--------------------------------------------------")
        return requestSecret
    else:
        print("接口请求失败--------------------------------------------------")


# 健康码查询
def jkm_query(appKey,sign):
    url = 'https://interface.zjzwfw.gov.cn/gateway/api/001003001/dataSharing/uU4lb0350783d2fa.htm'
    params = {
        'appKey': appKey,
        'sign': sign,
        'requestTime': time_stamp,
        'sfzh': result
    }
    response_jkm = requests.get(url,params)
    print(response_jkm.json())
    return response_jkm.json()


'''main 方法：主要方法是用于启动 - 调用方法'''
if __name__ == "__main__":
    # todo 1 程序开始时间
    startTime = datetime.datetime.now()
    print('\033[0;33;40m Program starts running 。。。 \033[0m')
    while True:
        result = db.execute('SELECT idcard FROM rkxx_sfz_ghc_temp ORDER BY RAND() LIMIT 1').fetchall()
        # 将本地时间转换为字符串，并格式化为时：分：秒
        c_time = time.strftime("%H:%M:%S", time.localtime())
        # 截取判断是否为整时
        if c_time[3:5] == '00':
            if c_time[6:8] =='00':
                print('现在是整点————', c_time)
                ran_list = random.sample(range(0, 59), random.randint(0, 5))
                ran_list = json.dumps(ran_list)
                r.set('list', ran_list)
        list = json.loads(r.get('list'))
        print(list)

        minute = int(datetime.datetime.now().strftime('%M'))
        for i in iter(list):
            if i == minute:
                print('开始调用接口-----------------------------')
                # todo 2 调用密钥方法
                appKey = 'A330881406627202107016701'
                appSecret = "e011fbb67ccb441c93dc18e9b2f2d86b"

                # 若有效期失效 重新获取签名
                if jkm_query(appKey, r.lindex('sign', -1).decode())['code'] != 00:
                    refreshSecret = get_refresh(appKey, md5value(appKey, appSecret))
                    requestSecret = get_secret(appKey, md5value(appKey, refreshSecret))

                    r.rpush('sign', md5value(appKey, requestSecret))
                    jkm_query(appKey, r.lindex('sign', -1).decode())

                # 若在15分钟有效期内
                else:
                    jkm_query(appKey, r.lindex('sign', -1).decode())
            else:
                break

        time.sleep(60)

    # todo 3 程序结束时间 并输出总耗时
    endTime = datetime.datetime.now()
    durTime = '\033[0;33;40m funtion time use:%dms \033[0m' % (
            (endTime - startTime).seconds * 1000 + (endTime - startTime).microseconds / 1000)
    print(durTime)

