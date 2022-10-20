# -*- coding: utf-8 -*- 
# @Time : 2021/12/8 20:42 
# @Author : J.wang 
# @File : py_thread.py
'''
    线程——Template
    使用线程池来执行线程任务的步骤如下：
        1、调用 ThreadPoolExecutor 类的构造器创建一个线程池。
        2、定义一个普通函数作为线程任务。
        3、调用 ThreadPoolExecutor 对象的 submit() 方法来提交线程任务。
        4、当不想提交任何任务时，调用 ThreadPoolExecutor 对象的 shutdown() 方法来关闭线程池。
    下面程序示范了如何使用线程池来执行线程任务：
'''
import redis, threading, time
from concurrent.futures import ThreadPoolExecutor


# 定义一个准备作为线程任务的函数
def action(max):
    my_sum = 0
    for i in range(max):
        print(threading.current_thread().name + '  ' + str(i))
        my_sum += i
    return my_sum


# 创建一个包含2条线程的线程池
pool = ThreadPoolExecutor(max_workers=2)
# 向线程池提交一个task, 50会作为action()函数的参数
future1 = pool.submit(action, 50)
# 向线程池再提交一个task, 100会作为action()函数的参数
future2 = pool.submit(action, 100)
# 判断future1代表的任务是否结束
print(future1.done())
time.sleep(3)
# 判断future2代表的任务是否结束
print(future2.done())
# 查看future1代表的任务返回的结果
print(future1.result())
# 查看future2代表的任务返回的结果
print(future2.result())
# 关闭线程池
pool.shutdown()
