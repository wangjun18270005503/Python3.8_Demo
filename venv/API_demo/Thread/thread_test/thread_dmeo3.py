# -*- coding: utf-8 -*- 
# @Time : 2021/12/9 10:21 
# @Author : J.wang 
# @File : thread_dmeo3.py
import requests
import json
import random
from multiprocessing import Pool,Manager,Lock
import multiprocessing
def register(sucess_count,failure_count,lock):
    data={'username': 'lily', 'password': 'wcx123wac', 'email': 'abc@qq.com'}
    data['username']='test'+str(random.randint(100,999))
    data=json.dumps(data)
    r=requests.post('http://39.106.41.11:8080/register/', data = data)
    code=r.status_code
    print (r.json())
    if r.json()['code']=='00':
        with lock:
            sucess_count.value+=1
    else:
        lock.acquire()
        failure_count.value += 1
        lock.release()
if __name__=='__main__':
    manager=Manager()
    lock=manager.Lock()
    sucess_count=manager.Value('i',0)
    failure_count=manager.Value('i',0)
    p=Pool()
    for i in range(multiprocessing.cpu_count()):
        p.apply_async(register,args=(sucess_count,failure_count,lock))
    p.close()
    p.join()
    print ('注册成功次数为：',sucess_count.value)
    print ('注册失败次数为：', failure_count.value)
