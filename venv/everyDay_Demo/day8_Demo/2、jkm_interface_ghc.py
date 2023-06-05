import requests, json, datetime, hashlib
import time

# appKey = 'A330881406627202107016701'
# appSecret = "e011fbb67ccb441c93dc18e9b2f2d86b"
time_stamp = str(int(time.time() * 1000))

#sign签名
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
    response = response.json()
    refreshSecret = response['datas']['refreshSecret']
    return refreshSecret

# 请求密钥
def get_secret(appKey,sign):
    url = 'http://interface.zjzwfw.gov.cn/gateway/app/refreshTokenBySec.htm'
    params = {
        'appKey': appKey,
        'sign': sign,
        'requestTime': time_stamp
    }
    response = requests.get(url,params)
    response = response.json()
    requestSecret = response['datas']['requestSecret']
    return requestSecret

# 健康码查询
def jkm_query(appKey,sign):
    url = 'https://interface.zjzwfw.gov.cn/gateway/api/001003001/dataSharing/uU4lb0350783d2fa.htm'
    params = {
        'appKey': appKey,
        'sign': sign,
        'requestTime': time_stamp
    }
    response = requests.get(url,params)
    print(response.json())


'''main 方法：主要方法是用于启动 - 调用方法'''
if __name__ == "__main__":
    # todo 1 程序开始时间
    startTime = datetime.datetime.now()
    print('\033[0;33;40m Program starts running 。。。 \033[0m')

    # todo 2 调用刷新密钥方法
    appKey = 'A330881406627202107016701'
    appSecret = "e011fbb67ccb441c93dc18e9b2f2d86b"
    md5value(appKey, appSecret)
    refreshSecret = get_refresh(appKey, md5value(appKey, appSecret))

    # 调用请求密钥方法
    appSecret = refreshSecret
    md5value(appKey, refreshSecret)
    requestSecret = get_secret(appKey,md5value(appKey, appSecret))

    # 调用刷新密钥方法
    appSecret = requestSecret
    md5value(appKey, requestSecret)
    jkm_query(appKey, md5value(appKey, requestSecret))


    # todo 3 程序结束时间 并输出总耗时
    endTime = datetime.datetime.now()
    durTime = '\033[0;33;40m funtion time use:%dms \033[0m' % (
            (endTime - startTime).seconds * 1000 + (endTime - startTime).microseconds / 1000)
    print(durTime)
