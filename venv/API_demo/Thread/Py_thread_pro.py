# -*- coding: utf-8 -*- 
# @Time : 2021/12/9 13:01
# @Author : J.wang
# @File : py_thread_demo2.py
'''
    (1) 接受外部传入参数： url：接口地址、appKey：应用key、appSecret：应用appSecret、loop_table_name：loop循环表、
                            create_name：需要创建对应的表名称、*params：param1、param2 接口循环入参参数英文名称
    (2) 发送接口请求：if签名错误：调用刷新密钥接口。
    (3) 请求成功：try：if create_name 已存在：数据插入 elif: 实现自动建表,插入数据  except e: finally: db.close() | cursor.close()
    (4) 附带线程查询数据
'''
from concurrent.futures import ThreadPoolExecutor
import threading
import re
import pymysql, json, math, random
import requests, time, redis, hashlib

requestTime = str(int(time.time() * 1000))
print('当前请求时间戳（毫秒）：' + requestTime)
# 连接 redis
r = redis.Redis(host='localhost', port=6379, db=1, decode_responses=True)


def split_list(valuesList,keyslist):
    # 线程列表
    new_value_list = []
    count_list = []
    keys_list = []
    print('\033[0;34;43m--待循环参数 keyslist：--\033[0m', keyslist,type(keyslist))
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
        print('\033[0;34;43m--待循环参数 new_list：--\033[0m', new_value_list, type(new_value_list))
        count_list.append(count)
        count += split_count
    return new_value_list, count_list,keys_list


def work1(new_list, count_list,keyslist):
    # sleep_time = random.randint(1, 5)  # 1~2 的随机沉睡时间
    # print('\033[0;33;40m\t1~5 的随机沉睡时间，当前为：\033[0m',sleep_time)
    print(f'当前获取列表的数据为： {new_list},线程名称：{threading.current_thread().name}')
    # print(f'当前获取列表的数据为： {df},\t沉睡时间： {sleep_time},list is {_list},线程名称：{threading.current_thread().name}')
    # time.sleep(sleep_time)
    print('\033[0;34;40m--待循环参数 new_list：--\033[0m', new_list)
    print('\033[0;34;40m--待循环参数 count_list：--\033[0m', count_list)
    print('\033[0;34;40m--待循环参数 keyslist：--\033[0m', keyslist)
    keyslist1 = tuple(keyslist)[0]
    print('\033[0;34;40m--待循环参数 keyslist_1：--\033[0m', keyslist1)

    param_str = '{' + ",".join('"' + str(keyslist1[n] + '":"' + str(new_list[0][n]) + '"') for n in range(len(keyslist1))) + '}'
    print('\033[0;34;40m--param_str：--\033[0m', param_str)
    gateway(url, appKey, appSecret, eval(param_str), create_name, table_comment)
    return sleep_time, new_list, count_list


def threadPool_new(valuesList, keyslist):
    with ThreadPoolExecutor(max_workers=pool_num) as pool:
        print('\033[0;34;40m--待循环参数 keyslist：--\033[0m', keyslist)
        print('\033[0;34;40m--待循环参数 valuesList：--\033[0m', valuesList)
        new_list, count_list,keys_list = split_list(valuesList,keyslist)
        # map返回一个迭代器，其中的回调函数的参数 最好是可以迭代的数据类型，如list；如果有 多个参数 则 多个参数的 数据长度相同；
        # 如： pool.map(work,[[1,2],[3,4]],[0,1]]) 中 [1,2]对应0 ；[3,4]对应1 ；其实内部执行的函数为 work([1,2],0) ; work([3,4],1)
        # map返回的结果 是 有序结果；是根据迭代函数执行顺序返回的结果
        # 使用map的优点是 每次调用回调函数的结果不用手动的放入结果list中
        results = pool.map(work1, new_list, count_list,keys_list)
        print(type(results))
        # 如下2行 会等待线程任务执行结束后 再执行其他代码
        # for ret in results:
        #     print(ret)
        print('thread execute end!')

# MD5 数据加工
def str_md5(str=''):
    md = hashlib.md5()
    md.update(str.encode(encoding="utf-8"))
    return md.hexdigest()


# （2）请求密钥
def refreshTokenBySec(appKey):
    refreshTokenBySec_Url = 'https://dw.qz.gov.cn/gateway/app/refreshTokenBySec.htm?'
    appSecret = r['refreshSecret']
    # 打印参数信息
    print('url：' + url + '\nappKey：' + appKey + '\nappSecret：' + appSecret)
    # todo 准备参数
    # (1) appKey  (参数自带)
    # (2) requestTime （获取当前时间戳）
    BySec_tiem = str(int(time.time() * 1000))
    # (3) sign
    str2_sign = appKey + appSecret + BySec_tiem
    sign1 = str_md5(str2_sign)
    # 组合参数
    params = {"appKey": appKey, "sign": sign1, "requestTime": BySec_tiem}
    response = requests.get(refreshTokenBySec_Url, params).json()
    print('\033[5;30;46m\t（2）请求密钥  接口返回参会参数：\033[0m', response)
    if response != None and response['code'] == '00':
        requestSecret = response['datas']['requestSecret']
        r.set('requestSecret', requestSecret)  # 设置 name 对应的值
        print('requestSecret：' + requestSecret)


# （1）刷新密钥
def refreshTokenByKey(appKey, appSecret):
    refreshTokenByKey_url = 'https://dw.qz.gov.cn/gateway/app/refreshTokenByKey.htm?'
    # 打印参数信息
    print('（1）刷新密钥', 'url：' + refreshTokenByKey_url + '\nappKey：' + appKey + '\nappSecret：' + appSecret)
    # todo 准备参数
    # (1) appKey  (参数自带)
    # (2) requestTime （获取当前时间戳）
    Bykey_tiem = str(int(time.time() * 1000))
    # (3) sign
    str1_sign = appKey + appSecret + Bykey_tiem
    sign = str_md5(str1_sign)
    # 组合参数
    params = {"appKey": appKey, "sign": sign, "requestTime": Bykey_tiem}
    response = requests.get(refreshTokenByKey_url, params).json()
    if response != None and response['code'] == '00':
        print('\033[5;30;46m\t（1）刷新密钥接口返回参会参数：\033[0m', response)
        # 存储至redis
        r = redis.Redis(host='localhost', port=6379, db=1, decode_responses=True)
        r.set('refreshSecret', response['datas']['refreshSecret'])  # 设置 name 对应的值
        refreshTokenBySec(appKey)


def insert_info(table_name, insert_columns, insert_values):
    db_inert = pymysql.Connect(host='127.0.0.1', user='root', password='159611', port=3306, database='python_mysql')
    cursor = db_inert.cursor()
    sql_insert_table = "insert into " + table_name + insert_columns + ' values ' + insert_values
    try:
        print('\033[5;30;46m\t开始插入数据 SQL \033[0m：', sql_insert_table)
        cursor.execute(sql_insert_table)
        db_inert.commit()
        print(cursor.rowcount)
    except Exception as e:
        db_inert.rollback()
        print("insert sql捕获到异常")
        raise e
    finally:
        if db_inert:
            print("关闭资源")
            cursor.close()
            db_inert.close()


def dict_column_comment_insert(create_name, table_comment, columns, dict_name):
    key_columns = columns  # 转存key
    value_columns = columns  # 转存value
    columns_v = '(' + ','.join('`' + str(column + "`") for column in key_columns.keys()) + ')'
    values_v = '(' + ','.join("'" + str(value_columns[column] + "'") for column in value_columns.keys()) + ')'
    table_name = 't_' + create_name + dict_name
    print('\033[0;33;40mtable_name:\033[0m', table_name, '\033[0;33;40m\tcolumns：\033[0m', columns_v,
          '\033[0;33;40m\tvalues：\033[0m', values_v)
    insert_info(table_name, columns_v, values_v)


# 循环解析
def fordict_insert(create_name, table_comment, for_dict, key_name):
    print('通用解析——插入数据 dict--------start--------!!!')
    if key_name != '': key_name = '_' + key_name
    dict_column_comment_insert(create_name, table_comment, for_dict, key_name)  # 组合sql
    for dd in for_dict.keys():
        table_name_last = '_' + dd
        if isinstance(for_dict[dd], dict):  # 判断是否为字典
            print('dict》》dict--------start--------')
            dict_column_comment_insert(create_name, table_comment, for_dict[dd], table_name_last)
            print(for_dict[dd])
            fordict_insert(create_name, table_comment, for_dict[dd], dd)
        elif isinstance(for_dict[dd], list):
            print('dict》》list--------start--------')
            dict_column_comment_insert(create_name, table_comment, for_dict[dd][0], table_name_last)
            fordict_insert(create_name, table_comment, for_dict[dd][0], dd)
        else:
            pass
            # print('当前不进行解析！' + dd)
            # return
    print('dict -------- end --------')


def create_table(create_name, table_comment, column_comment):
    print('开始自动建表！！！')
    try:
        db = pymysql.Connect(host='127.0.0.1', user='root', password='159611', port=3306, database='python_mysql')
        cursor = db.cursor()
        table_exists_sql = "SHOW TABLES;"
        cursor.execute(table_exists_sql)
        table_exists_list = cursor.fetchall()
        table_list = re.findall('(\'.*?\')', str(table_exists_list))
        table_list = [re.sub("'", '', each) for each in table_list]
        if create_name in table_list:
            print('\033[0;33;40m\t数据库中同名表已存在无需创建,直接插入数据：\033[0m', 0)
        else:
            print('\033[0;33;40m\t不存在进行表创建：\033[0m')
            sql_create_table = "CREATE TABLE if not exists " + create_name + """
                    (`id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',""" + column_comment + """       
                    `remarks` varchar(100) NOT NULL DEFAULT '' COMMENT '备注',
                    `update_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '修改时间',
                    `update_by` varchar(60) NOT NULL DEFAULT '1',
                    `create_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                    `create_by` varchar(60) NOT NULL DEFAULT '1',
                    `del_flag` char(1) NOT NULL DEFAULT '0' COMMENT '0正常，1删除',
                    PRIMARY KEY (`id`)
                     ) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8mb4 COMMENT='""" + table_comment + "';"
            print(sql_create_table)
            cursor.execute(sql_create_table)
            db.commit()
            print(cursor.rowcount)
    except pymysql.Error as e:
        print("数据库连接失败：" + str(e))
    finally:
        if db:
            db.close()
            cursor.close()
            print('关闭数据库连接....')


def dict_column_comment_create(create_name, table_comment, columns, dict_name):
    print(columns)
    print('dict_name：' + dict_name)
    column_str = ",".join(
        "`" + str(column + "` varchar(100) NOT NULL DEFAULT '' COMMENT ''") for column in (columns).keys()) + ','
    create_name = 't_' + create_name + dict_name
    print(create_name)
    create_table(create_name, table_comment, column_str)
    return column_str


def list_column_comment_create(create_name, table_comment, columns, dict_name):
    print(type(columns))
    print(columns)
    return ",".join(
        "'" + str(columns[i] + "' varchar(100) NOT NULL DEFAULT '' COMMENT ''") for i in range(len(columns)))


def fordict_create(create_name, table_comment, for_dict, key_name):
    print('通用建表 dict!!!')
    print('dict --------start--------')
    if key_name != '': key_name = '_' + key_name
    column_str = dict_column_comment_create(create_name, table_comment, for_dict, key_name)  # 组合sql
    print(column_str)
    for dd in for_dict.keys():
        table_name_last = '_' + dd
        if isinstance(for_dict[dd], dict):  # 判断是否为字典
            print('dict》》dict--------start--------')
            print(dict_column_comment_create(create_name, table_comment, for_dict[dd], table_name_last))
            print(for_dict[dd])
            fordict_create(create_name, table_comment, for_dict[dd], dd)
        elif isinstance(for_dict[dd], list):
            print('dict》》list--------start--------')
            print(dict_column_comment_create(create_name, table_comment, for_dict[dd][0], table_name_last))
            fordict_create(create_name, table_comment, for_dict[dd][0], dd)
        else:
            pass
            # print('当前不进行解析！' + dd)
            # return
    print('dict -------- end --------')


def fordata(create_name, table_comment, contents):
    for key in contents.keys():
        # 判断 是否为列表
        if (key == 'datas' or key == 'data') and isinstance(contents[key], list):
            fordict_create(create_name, table_comment, contents[key][0], '')
            fordict_insert(create_name, table_comment, contents[key][0], '')
        # 判断 是否为字典
        if (key == 'datas' or key == 'data') and isinstance(contents[key], dict):
            fordict_create(create_name, table_comment, contents[key], '')
            fordict_insert(create_name, table_comment, contents[key], '')


# 定义方法传参形式
def gateway(url, appKey, appSecret, key_value, create_name, table_comment):
    # todo 准备参数
    # (1) appKey  (参数自带)
    # (2) requestTime （获取当前时间戳）
    # (3) sign
    ApiappSecret = r['requestSecret']
    str = appKey + ApiappSecret + requestTime
    sign = str_md5(str)
    # (4) 业务参数  (查询接口配置信息)
    # 组合参数
    params = {"appKey": appKey, "sign": sign, "requestTime": requestTime}
    param_dict = params.update(key_value)
    print('\033[0;33;40m请求参数：\033[0m', params)
    response = requests.get(url, params).json()
    print('\033[5;30;46m\t接口返回参会参数：\033[0m', response)
    if response != None and response['code'] == '00':
        # 存储数据
        print('\033[0;33;40m\t开始插入数据：\033[0m')
        fordata(create_name, table_comment, response)
    else:
        print('签名错误')
        refreshTokenByKey(appKey, appSecret)


def ApiBatchRetained_select(url, appKey, appSecret, loop_table_name, create_name, table_comment, pool_num, *params):
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
        param_list = cursor.fetchmany(1000)  # 指定循环次数
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

        # # 传参、调用接口
        # for i in range(len(param_list)):
        #     print('paramsssss:',params)
        #     param_str = '{' + ",".join(
        #         '"' + str(params[n] + '":"' + str(param_list[i][n]) + '"') for n in range(len(params))) + '}'
        #     print('param_strssss：',param_str)
        # gateway(url, appKey, appSecret, eval(param_str), create_name, table_comment)
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
    table_comment = '测试自动建表'
    pool_num = 10  # 线程数
    param = 'cardId'
    param2 = 'name'
    print('startTiem', str(int(time.time() * 1000)))
    ApiBatchRetained_select(url, appKey, appSecret, loop_table_name, create_name, table_comment, pool_num, param,
                            param2)
    print('endTiem', str(int(time.time() * 1000)))
