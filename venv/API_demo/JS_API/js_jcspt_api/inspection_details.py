# -*- coding: utf-8 -*-
# @Time : 2021/11/27 16:45
# @Author : ChenXin
# @File : inspection_details.py
# @Effect ：获取巡查记录详情
import json
import pymysql
import requests
import redis



# 连接 redis
r = redis.Redis(host='10.50.207.215', port=6379, db=6, password='sx123456', decode_responses=True)
# 取出redis中的auth：
auth = r['access_token']
# print auth

# 数据库链接
govdb = pymysql.Connect(host='127.0.0.1', user='root', password='159611', port=3306,database='python_mysql')
# 使用cursor()方法获取操作游标
govtest_cursor = govdb.cursor()
# 查询入参id
selectsql = "SELECT id FROM loop_recordinfo_id WHERE del_flag='0'"
# 执行SQL语句
govtest_cursor.execute(selectsql)
# 操作查询出的id
results = govtest_cursor.fetchall()

# 更新数据表del_flag
# updatesql = "UPDATE local_tqxtdj_xcjlxq set del_flag='1'"
# # 执行SQL
# govtest_cursor.execute(updatesql)

# pu = []
for row in results:
    # 入参id(row[0])
    # pu.append(row[0])
    # 接口地址
    url = "http://gateway.daliandong.cn/api/jczl_prod_quzhou/patrol/getRecordById.json"
    # 头部
    headers = {'auth': auth}
    # 数据
    # data = {'appKey':"MBMAWSCLUWYWBAAKMQEH",'bizContent':"{'id':'1394629262257950745'}"}
    data = {'appKey': "MBMAWSCLUWYWBAAKMQEH", 'bizContent': "{'id':" + row[0] + "}"}
    # 请求接口
    respose = requests.post(url, data=data, headers=headers)
    # 调用接口
    message = respose.text
    # print message
    # 解析接口
    pt = json.loads(message)
    # visitRecord = pt['data']['visitRecord']
    # print  visitRecord['changeIssueType']

    # 所属区域
    checkOrgName = pt['data']['checkOrgName']
    # 备注、检查地址
    visitRecord = pt['data']['visitRecord']

    # 检查结果
    rcqjqk = "";
    gzqk = "";
    wlryqk = "";
    sxdt = "";
    llfy = "";

    # 获取检查情况
    for i in pt['data']['checkPointRecordVOs']:
        # print i['checkPointRecord']['visitRecordId'],i['checkPointRecord']['checkPointName'],i['checkPointRecord']['passResult']

        if (i['checkPointRecord']['checkPointName'] == "日常起居情况"):
            rcqjqk = i['checkPointRecord']['passResult']
        elif (i['checkPointRecord']['checkPointName'] == "工作情况"):
            gzqk = i['checkPointRecord']['passResult']
        elif (i['checkPointRecord']['checkPointName'] == "往来人员情况"):
            wlryqk = i['checkPointRecord']['passResult']
        elif (i['checkPointRecord']['checkPointName'] == "思想动态"):
            sxdt = i['checkPointRecord']['passResult']
        elif (i['checkPointRecord']['checkPointName'] == "邻里反映"):
            llfy = i['checkPointRecord']['passResult']

    # 获取附件信息
    for i2 in pt['data']['remarkFiles']:
        if (i['checkPointRecord']['visitRecordId'] == i2['visitRecordId']):
            a = i2['visitRecordId']
        # 插入数据表
        insertsql = "insert into local_tqxtdj_xcjlxq(id,rcqjqk,gzqk,wlryqk,sxdt,llfy,checkAddress,remark,\
                     visitRecordId,internalUrl,checkOrgName,checkUserName,peerChecker,checkDate) values \
                    ('%s', '%s', '%s','%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
                    (i['checkPointRecord']['visitRecordId'], rcqjqk, gzqk, wlryqk, sxdt, llfy,
                     visitRecord['checkAddress'], visitRecord['remark'], a, \
                     i2['downloadFileVO']['internalUrl'], visitRecord['checkUserName'],checkOrgName, visitRecord['peerChecker'],
                      visitRecord['checkDate'])

        print (i['checkPointRecord']['visitRecordId'], rcqjqk, gzqk, wlryqk, sxdt, llfy, visitRecord['checkAddress'], \
        visitRecord['remark'], a,visitRecord['checkUserName'], visitRecord['peerChecker'], checkOrgName, visitRecord['checkDate'], \
        i2['downloadFileVO']['internalUrl'])

    # 执行SQL
    govtest_cursor.execute(insertsql)
    # 提交
    govdb.commit()
