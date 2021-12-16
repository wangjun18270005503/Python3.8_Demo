# -*- coding: utf-8 -*- 
# @Project ：Git_Python3.8_Demo 
# @Time : 2021/12/10 16:18 
# @Author : J.wang 
# @Version：V 0.1 
# @File : py_insert_demo1.py
# @Software: PyCharm
# @desc : 插入数据返回 主键id
import pymysql
db = pymysql.Connect(host='127.0.0.1',user='root',password='159611',port=3306,database='python_mysql')
print()