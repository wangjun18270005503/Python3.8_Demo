#2022/9/30 全省健康码查询 接口练习
import requests
import datetime
import time
# 在python3中使用hashlib模块进行md5操作
import hashlib

appKey = "A330881406627202107016701"

# 字符串进行md5加密
def md5(str):
    # 创建md5对象
    m = hashlib.md5()
    m.update(str.encode("utf8"))
    return m.hexdigest()

#获得13位时间戳
def get_time_stamp13():
    # 生成13时间戳   eg:1540281250399895
    datetime_now = datetime.datetime.now()
    # 10位，时间点相当于从UNIX TIME的纪元时间开始的当年时间编号
    date_stamp = str(int(time.mktime(datetime_now.timetuple())))
    # 3位，微秒
    data_microsecond = str("%06d"%datetime_now.microsecond)[0:3]
    date_stamp = date_stamp+data_microsecond
    return str(date_stamp)

def get_way(app_getsecret,u):
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

def post_way(app_postsecret):
    appSecret = app_postsecret
    mkt = get_time_stamp13()
    str_md5 = appKey + appSecret + str(mkt)
    sign = md5(str_md5)
    data_dict = {
        "appKey": appKey,
        "sign": sign,
        "requestTime": mkt,
        "sfzh": "500236200108211304"
    }
    url = "https://interface.zjzwfw.gov.cn/gateway/api/001003001/dataSharing/uU4lb0350783d2fa.htm?"
    headers = {}
    response = requests.post(url=url, headers=headers, data=data_dict)
    rep_obj =response.json()
    return rep_obj


def refresh_key():
    ref_dict = get_way("e011fbb67ccb441c93dc18e9b2f2d86b","http://interface.zjzwfw.gov.cn/gateway/app/refreshTokenByKey.htm?")
    print(ref_dict)
    # print(ref_dict["datas"]['refreshSecret'])
    return ref_dict["datas"]['refreshSecret']

def request_key():
    ref_appsecret = refresh_key()
    # ref_appsecret = "0cbe8e3aec4f4edb8d45716eeaa3f3c3"
    req_dict = get_way(ref_appsecret,'http://interface.zjzwfw.gov.cn/gateway/app/refreshTokenBySec.htm?')
    print(req_dict)
    return req_dict["datas"]['requestSecret']

def JKM_search():
    se_appsecret = request_key()
    # se_appsecret = "33dc1dc19dba456f91a16a34d16d7a9e"
    se_dict = post_way(se_appsecret)
    print(se_dict)

if __name__ == "__main__":
    print("\033[0;32m%s\033[0m" % u"===================start===================")
    print(u"开始时间：", datetime.datetime.now())

    JKM_search()

    print(u"结束时间：", datetime.datetime.now())
    print("\033[0;31m%s\033[0m" % u"总共耗时：", datetime.datetime.now() - datetime.datetime.now())
    print("\033[0;32m%s\033[0m" % u"===================stop===================")