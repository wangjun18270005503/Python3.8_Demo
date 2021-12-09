# -*- coding: utf-8 -*-
# @Time : 2021/12/8 22:01
# @Author : J.wang
# @File : py_thread_demo2.py
import math
import random
import threading
import time
from concurrent.futures import ThreadPoolExecutor

# 按规则 拆分数据
def split_list(param_list):
    # 线程列表
    new_param_list = []
    count_list = []
    # 每个线程处理的数据大小
    split_count = 1
    # 需要的线程个数
    times = math.ceil(len(param_list) / split_count)
    count = 0
    for item in range(times):
        params = param_list[count: count + split_count]
        # print('params',params)
        new_param_list.append(params)  # 已处理的数据存放到
        # print('new_param_list',new_param_list)
        count_list.append(count)   # 计算 处理次数
        # print('count_list',count_list)
        count += split_count
    return new_param_list, count_list


def work1(df, _list):
    print(f'当前获取列表的数据为： {df},线程名称：{threading.current_thread().name}')
    return  df, _list


def threadPool_new(param_list):
    with ThreadPoolExecutor(max_workers=5) as pool:
        new_list, count_list = split_list(param_list)  # 调用方法拆分数据
        print('new_list',new_list)
        print('count_list：',count_list)
        results = pool.map(work1, new_list, count_list)
        print(type(results))
        # 如下2行 会等待线程任务执行结束后 再执行其他代码
        # for ret in results:
        #     print(ret)
        print('thread execute end!')


if __name__ == '__main__':
    # 需要处理的数据
    param_list = ['张三', '李四', '王五', '马六', '田六', '小七', '八哥', '九妹', '十一', 10]
    threadPool_new(param_list)
