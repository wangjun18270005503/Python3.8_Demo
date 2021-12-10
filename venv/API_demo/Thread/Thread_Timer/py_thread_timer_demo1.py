# -*- coding: utf-8 -*- 
# @Project ：Git_Python3.8_Demo 
# @Time : 2021/12/9 22:33 
# @Author : J.wang 
# @Version：V 0.1 
# @File : py_thread_timer_demo1.py
# @Software: PyCharm
# @desc : 线程定时器 Timer
'''
    参数：
        interval——定时器间隔 间隔多少秒之后启动定时器任务（单位秒）
        function——线程函数
        args——线程参数，可传递元组类型数据，默认为空（缺省参数）
        kwargs——线程参数，可以传递字典类型数据，默认为空（缺省参数）
'''
import threading
from datetime import datetime
from threading import Timer
import time

timer = threading.Timer(interval='', function='', args='', kwargs='')


def timedTask():
    '''
        第一个参数：延迟多长时间执行任务（单位：秒）
        第二个参数：要执行的任务，即函数
        第三个参数：调用函数的参数（tuple）
        :return:
    '''
    Timer(10, task, ()).start()


# 任务
def task():
    print('当前时间',datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


if __name__ == '__main__':
    timedTask()
    while True:
        print(time.time())
        time.sleep(5)
