# -*- coding: utf-8 -*- 
# @Time : 2021/12/9 10:23 
# @Author : J.wang 
# @File : thread_demo4.py
'''
    线程 启动线程
'''
import math
import random
import threading
import time
from concurrent.futures import ThreadPoolExecutor


def split_key_list(keysList):
    pass


def split_list(valuesList,keyslist):
    # 线程列表
    new_value_list = []
    count_list = []
    keys_list = []
    print('\033[0;34;43m--待循环参数 keyslist：--\033[0m', keyslist,type(keyslist))
    # 每个线程处理的数据大小
    split_count = 1
    # 需要的线程个数
    times = math.ceil(len(valuesList) / split_count)
    count = 0
    for item in range(times):
        keys_list.append(keyslist)
        value_list = valuesList[count: count + split_count]
        # print('\033[0;34;43m--待循环参数 value_list：--\033[0m', value_list, type(value_list))
        new_value_list.append(value_list)
        print('\033[0;34;43m--待循环参数 new_list：--\033[0m', new_value_list, type(new_value_list))
        count_list.append(count)
        count += split_count
    return new_value_list, count_list,keys_list


def work1(new_list, count_list,keyslist):
    # sleep_time = random.randint(1, 5)  # 1~2 的随机沉睡时间
    # print('\033[0;33;40m\t1~5 的随机沉睡时间，当前为：\033[0m',sleep_time)
    print(f'当前获取列表的数据为： {new_list},线程名称：{threading.current_thread().name}')
    # print(f'当前获取列表的数据为： {df},\t沉睡时间： {sleep_time},list is {_list},线程名称：{threading.current_thread().name}')
    # time.sleep(sleep_time)
    print('\033[0;34;40m--待循环参数 new_list：--\033[0m', new_list)
    print('\033[0;34;40m--待循环参数 count_list：--\033[0m', count_list)
    print('\033[0;34;40m--待循环参数 keyslist：--\033[0m', keyslist)
    keyslist1 = tuple(keyslist)[0]
    print('\033[0;34;40m--待循环参数 keyslist_1：--\033[0m', keyslist1)

    param_str = '{' + ",".join('"' + str(keyslist1[n] + '":"' + str(new_list[0][n]) + '"') for n in range(len(keyslist1))) + '}'
    print('\033[0;34;40m--param_str：--\033[0m', param_str)

    return sleep_time, new_list, count_list


def threadPool_new(valuesList, keyslist):
    with ThreadPoolExecutor(max_workers=1) as pool:
        print('\033[0;34;40m--待循环参数 keyslist：--\033[0m', keyslist)
        print('\033[0;34;40m--待循环参数 valuesList：--\033[0m', valuesList)
        new_list, count_list,keys_list = split_list(valuesList,keyslist)
        # map返回一个迭代器，其中的回调函数的参数 最好是可以迭代的数据类型，如list；如果有 多个参数 则 多个参数的 数据长度相同；
        # 如： pool.map(work,[[1,2],[3,4]],[0,1]]) 中 [1,2]对应0 ；[3,4]对应1 ；其实内部执行的函数为 work([1,2],0) ; work([3,4],1)
        # map返回的结果 是 有序结果；是根据迭代函数执行顺序返回的结果
        # 使用map的优点是 每次调用回调函数的结果不用手动的放入结果list中
        results = pool.map(work1, new_list, count_list,keys_list)
        print(type(results))
        # 如下2行 会等待线程任务执行结束后 再执行其他代码
        # for ret in results:
        #     print(ret)
        print('thread execute end!')


if __name__ == '__main__':
    # 需要处理的数据
    valuesDict = (('140104195807050813', '毛永森'), ('140303198012310018', '刘斌'), ('142723197904180700', '李风丹'),
                  ('152125196610130529', '鲁代林'), ('152126194910282425', '周冬仙'), ('152127200103250026', '魏恒佳'),
                  ('152224195301011029', '陈素芝'), ('210423194205070031', '石德久'), ('210621197805061085', '王丽荣'),
                  ('211302198011061227', '葛志红'))
    keysDict = []
    keys = ('cardId', 'name')
    keysDict.append(keys)
    threadPool_new(list(valuesDict), list(keysDict))
