# -*- coding: utf-8 -*- 
# @Project ：Git_Python3.8_Demo 
# @Time : 2021/12/14 9:08 
# @Author : J.wang 
# @Version：V 0.1 
# @File : yaml_demo.py
# @Software: PyCharm
# @desc :

import pymysql
import yaml,apply

f = open(r'../common/sx_dataServer.yml', encoding='utf-8')
y = yaml.load(f, Loader=yaml.FullLoader)
print(y)

file = open(r'../common/sx_dataServer.yml', encoding='utf-8')
file_data = file.read()
file.close()
data = yaml.load(file_data, Loader=yaml.FullLoader)
db_local = data['db_local']
print(db_local)
db = pymysql.Connect(host=db_local['host'], user=db_local['user'], password=db_local['password'],
                     port=int(db_local['port']), database=db_local['database'])
cursor = db.cursor()
table_exists_sql = "SHOW TABLES;"
cursor.execute(table_exists_sql)
table_exists_list = cursor.fetchall()
print(table_exists_list)
db.close()

