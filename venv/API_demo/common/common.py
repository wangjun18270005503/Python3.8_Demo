# -*- coding: utf-8 -*- 
# @Time : 2021/12/6 14:48 
# @Author : J.wang 
# @File : common.py

import requests,time,datetime,hashlib
import redis   # 导入redis 模块
# MD5 数据加工
def str_md5(str = ''):
    md = hashlib.md5()
    md.update(str.encode(encoding="utf-8"))
    return md.hexdigest()

# 存储 redis 键值对
def set_redis(ip,port,db,name,value):
    r = redis.Redis(host=ip, port=port, db=db, decode_responses=True)
    r.set(name,value)  # 设置 name 对应的值
    print(r[name])
    print(r.get(name))  # 取出键 name 对应的值
    print(type(r.get(name)))  # 查看类型