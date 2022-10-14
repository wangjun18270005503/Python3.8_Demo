# -*- coding: utf-8 -*- 
# @Project ：Git_Python3.8_Demo 
# @Time : 2022/3/3 16:31 
# @Author : J.wang 
# @Version：V 0.1 
# @File : demo3.py
# @Software: PyCharm
# @desc :
# 折线图   https://blog.csdn.net/weixin_44279178/article/details/108203167
# 将柱状图和折线图放在一个图中
from pyecharts import Bar, Line
from pyecharts import Overlap
name_list = ["冰箱", "电视", "空调", "电脑"]#属性名称
value_list0 = [15, 25, 5, 10]#属性值0
value_list1 = [5, 10, 15, 20]#属性值1
bar = Bar(title="水果销量")
line = Line()
bar.add("商家0", name_list, value_list0, mark_line=["average"], mark_point=["max", "min"], is_label_show=True)#将数据加入图中
bar.add("商家1", name_list, value_list1, mark_line=["average"], mark_point=["max", "min"], is_label_show=True)#将数据加入图中
line.add("商家0", name_list, value_list0, is_smooth=True)#将数据加入图中
line.add("商家1", name_list, value_list1)#将数据加入图中
overlap = Overlap()
overlap.add(bar)
overlap.add(line)
overlap.render('./柱状图+折线图.html')
