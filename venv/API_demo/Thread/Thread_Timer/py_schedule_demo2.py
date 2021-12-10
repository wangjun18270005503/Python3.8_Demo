# -*- coding: utf-8 -*- 
# @Project ：Git_Python3.8_Demo 
# @Time : 2021/12/9 23:05 
# @Author : J.wang 
# @Version：V 0.1 
# @File : py_schedule_demo2.py
# @Software: PyCharm
# @desc :
import datetime
import schedule
import time


def func():
    now = datetime.datetime.now()
    ts = now.strftime('%Y-%m-%d %H:%M:%S')
    print('do func  time :', ts)


def func2():
    now = datetime.datetime.now()
    ts = now.strftime('%Y-%m-%d %H:%M:%S')
    print('do func2 time：', ts)


def tasklist():
    # 清空任务
    schedule.clear()
    # 创建一个按秒间隔执行任务
    schedule.every(1).minutes.do(func)
    # 创建一个按2秒间隔执行任务
    schedule.every(2).minutes.do(func2)
    # 执行10S
    for i in range(100000):
        schedule.run_pending()
        time.sleep(1)


tasklist()
