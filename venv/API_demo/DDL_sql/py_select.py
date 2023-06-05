# -*- coding: utf-8 -*- 
# @Time : 2021/12/7 15:00 
# @Author : J.wang 
# @File : py_select.py
import pymysql, re
db = pymysql.Connect(host='**.**.**.210', user='x*z*x*', password='X*z*c*1234', port=3306, database='x*z*x*')
cursor = db.cursor()
sql = "SELECT id,name,sex,age,id_card,disabled_type,disabled_level,credit,credit_amount,credit_name,credit_date,channel_time,origin_domicile_addr,new_domicile_addr,reside_addr,create_date,street,allowance,work,subsidy,self FROM	`dp_fraud_disabled_info` WHERE credit_name !='' AND origin_domicile_addr IS NOT NULL AND new_domicile_addr IS NOT NULL AND reside_addr IS NOT NULL AND street IS NOT NULL LIMIT 1,10;"

# 执行SQL
cursor.execute(sql)
info = cursor.fetchall()
print(info)
# 提交
db.commit()
db.close()
cursor.close()