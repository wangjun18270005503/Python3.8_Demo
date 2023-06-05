# -*- coding: utf-8 -*- 
# @Project ：Git_Python3.8_Demo 
# @Time : 2021/12/28 19:13 
# @Author : J.wang 
# @Version：V 0.1 
# @File : record_info_thread.py
# @Software: PyCharm
# @desc : 启动线程池

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
        print('---------------------',count_list)
        count += split_count
    return new_value_list, count_list, keys_list


def work1(new_list, count_list, keyslist):
    sleep_time = random.randint(1, 5)  # 1~2 的随机沉睡时间
    print('\033[0;33;40m\t1~5 的随机沉睡时间，当前为：\033[0m',sleep_time)
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


# MD5 数据加工
def str_md5(str=''):
    md = hashlib.md5()
    md.update(str.encode(encoding="utf-8"))
    return md.hexdigest()


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


def insert_info(table_name, insert_columns, insert_values):
    db_inert = pymysql.Connect(host='127.0.0.1', user='root', password='159611', port=3306, database='python_mysql')
    cursor = db_inert.cursor()
    sql_insert_table = "insert into " + table_name + insert_columns + ' values ' + insert_values
    print('***************',sql_insert_table)
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
                    (`id_i` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',""" + column_comment + """       
                    `remarks` varchar(100) NOT NULL DEFAULT '' COMMENT '备注',
                    `update_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '修改时间',
                    `update_by` varchar(60) NOT NULL DEFAULT '1',
                    `create_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                    `create_by` varchar(60) NOT NULL DEFAULT '1',
                    `del_flag` char(1) NOT NULL DEFAULT '0' COMMENT '0正常，1删除',
                    PRIMARY KEY (`id_i`)
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
def gateway(url, appKey, username, password, key_value, create_name, table_comment):
    # todo 准备参数
    # # 请求头
    auth = r['access_token']
    record_info_headers = {'auth': auth}
    print('++++++++++请求参数id++++++++++', key_value)

    # (4) 业务参数  (查询接口配置信息)
    # 组合参数
    params = {'appKey': "MBMAWSCLUWYWBAAKMQEH", 'bizContent':str(key_value)}
    # param_dict = params.update(key_value)
    print('\033[0;33;40m请求参数：\033[0m', params)
    response = requests.post(url, data=params, headers=record_info_headers).json()
    print('\033[5;30;46m\t接口返回参会参数：\033[0m', response)

    if response != None and response['success'] :
        # 存储数据
        print('\033[0;33;40m\t开始插入数据：\033[0m')
        fordata(create_name, table_comment, response)
        print('开始插入数据')
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
        param_list = cursor.fetchmany(2)  # 指定循环次数
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
        if db:
            db.close()
            print('关闭数据库连接....')


# 调用方法 刷新请求密钥方法
if __name__ == "__main__":
    print('startTiem', str(int(time.time() * 1000)))
    # 业务接口地址
    url = 'http://gateway.daliandong.cn/api/jczl_prod_quzhou/patrol/getRecordById.json'
    appkey = 'MBMAWSCLUWYWBAAKMQEH'
    username = 'Azdry01@qzsg'
    password = 'afdd0b4ad2ec172c586e2150770fbf9e'
    loop_table_name = 'loop_recordinfo_id'
    create_name = 'local_tqxtdj_info'
    table_comment = '政法委基层四平台巡查记录详情'
    pool_num = 1  # 线程数
    param = 'id'
    # param2 = 'name'
    ApiBatchRetained_select(url, appkey, username, password, loop_table_name, create_name, table_comment, pool_num,
                            param)
    # refreshTokenByKey(appkey, username, password)
    print('endTiem', str(int(time.time() * 1000)))
