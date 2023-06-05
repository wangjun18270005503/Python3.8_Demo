# -*- coding: utf-8 -*-
# @Time : 2021/11/2 17:20
# @Author : ChenXin
# @File : **.py
# @Effect ：
import json
import urllib2

import MySQLdb
import requests
import sys
import redis

reload(sys)
sys.setdefaultencoding("utf-8")

# 打开数据库连接_所需监控的表
govdb = MySQLdb.connect("**.**.**.210", "x*z*x*", "X*z*c*1234", "sx_local_govern_test",charset='utf8')

# 使用cursor()方法获取操作游标
govtest_cursor = govdb.cursor()

pagecount="1"

url = "http://gateway.daliandong.cn/api/jczl_prod_quzhou/basePplUnify/getKeyPersons.json"
headers = {'auth':'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0ZW5hbnRfaWQiOiIzMzA4MDAiLCJjb2RlIjoyMDAsInJvbGVfY29kZXMiOm51bGwsInVzZXJfbmFtZSI6IkF6ZHJ5MDFAcXpzZyIsImNsaWVudF9pZCI6InVzZXJjZW50ZXIiLCJyb2xlX2lkcyI6bnVsbCwiYWRtaW5pc3RyYXRvciI6ZmFsc2UsInVzZXJfaWQiOiIxNDczNTc5Njg3OTU4NTUyNjczIiwib3JnX2lkIjoiMTAxMjI5Nzc4MTM0NTI3MTgwOSIsInN1Y2Nlc3MiOnRydWUsInNjb3BlIjpbImFsbCJdLCJvYXV0aF9pZCI6IiIsImV4cCI6MTY0MDYxMzM2NiwianRpIjoiZWQyZGRlNzgtM2FjNC00ODlhLWI2YjYtNGZhYzg2NDVjZjJiIn0._Owfv0JDrBTdrF95K0gJcJJcwvEkv5T8_asiZnFvG2g'}
data = {'appKey':"MBMAWSCLUWYWBAAKMQEH",'bizContent':"{'departmentNo':'330881','keyPersonType':'base_ppl_others','page':"+pagecount+",'rows':'400'}"}
respose = requests.post(url,data=data,headers=headers)

message=respose.text

pt = json.loads(message)


for i in pt['data']['records']:
    print i['cardId'],i['orgName'],i['basePplExpandId'],i['name'],i['id'],i['orgId'],i.setdefault('inhabitedArea',''),i.setdefault('residenceAddrRk',''),i['extendType']

    # 插入数据表
    sql = "insert into sx_local_govern_test.tqxtdj_zdrylb(cardId,orgName,basePplExpandId,name,id,orgId,inhabitedArea,residenceAddrRk,extendType) values ('%s', '%s', '%s','%s', '%s', '%s','%s', '%s', '%s')" \
        %(i['cardId'],i['orgName'],i['basePplExpandId'],i['name'],i['id'],i['orgId'],i.setdefault('inhabitedArea',''),i.setdefault('residenceAddrRk',''),i['extendType'])

    #执行SQL
    govtest_cursor.execute(sql)
    # 提交
    govdb.commit()

govdb.close()