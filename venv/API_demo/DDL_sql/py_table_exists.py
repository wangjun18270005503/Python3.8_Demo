# -*- coding: utf-8 -*- 
# @Time : 2021/12/8 15:12 
# @Author : J.wang 
# @Version：V 0.1
# @File : py_table_exists.py
# @desc : 判断表是否才能在
import pymysql
import re


def table_exists(con, table_name):  # 这个函数用来判断表是否存在
    sql = "show tables;"
    con.execute(sql)
    tables = [con.fetchall()]
    table_list = re.findall('(\'.*?\')', str(tables))
    table_list = [re.sub("'", '', each) for each in table_list]
    if table_name in table_list:
        return 1  # 存在返回1
    else:
        return 0  # 不存在返回0


connect = pymysql.connect(user='root', password='159611', host='127.0.0.1', database='python_mysql', port=3306, charset='utf8')
con = connect.cursor()
con.execute(sql)
table_name = 'animal'
if (table_exists(con, table_name) != 1):
    print("表不存在，可以添加一张")

con.close()
connect.close()