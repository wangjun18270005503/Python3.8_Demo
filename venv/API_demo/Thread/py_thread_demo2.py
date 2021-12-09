# -*- coding: utf-8 -*- 
# @Time : 2021/12/8 22:01 
# @Author : J.wang 
# @File : py_thread_demo2.py
'''
此外，Exectuor 还提供了一个 map(func, *iterables, timeout=None, chunksize=1) 方法，该方法的功能类似于全局函数 map()，区别在于线程池的 map() 方法会为 iterables 的每个元素启动一个线程，以并发方式来执行 func 函数。这种方式相当于启动 len(iterables) 个线程，井收集每个线程的执行结果。
例如，如下程序使用 Executor 的 map() 方法来启动线程，并收集线程任务的返回值：
'''
from concurrent.futures import ThreadPoolExecutor
import threading
import time


# 定义一个准备作为线程任务的函数
def action(max):
    my_sum = 0
    for i in range(max):
        print(threading.current_thread().name + '  ' + str(i))
        my_sum += i
    return my_sum


# 创建一个包含4条线程的线程池
with ThreadPoolExecutor(max_workers=10) as pool:
    # 使用线程执行map计算
    # 后面元组有3个元素，因此程序启动3条线程来执行action函数
    results = pool.map(action, (50, 100, 150, 200, 250, 300, 350))
    print('--------------')
    for r in results:
        print(r)