# -*- coding: utf-8 -*- 
# @Project ：Git_Python3.8_Demo 
# @Time : 2022/3/3 16:26 
# @Author : J.wang 
# @Version：V 0.1 
# @File : demo1.py
# @Software: PyCharm
# @desc :
from pyecharts.charts import WordCloud

name = ['云想衣裳花想容','春风拂槛露华浓','若非群玉山头见','会向瑶台月下逢','一枝秾艳露凝香','云雨巫山枉断肠',
'借问汉宫谁得似','可怜飞燕倚新妆','名花倾国两相欢','长得君王带笑看','解释春风无限恨','沈香亭北倚阑干']
value = [945,760,389,209,250,450,850,560,780,150]
data = list(zip(name, value))

mywordcloud = WordCloud()
mywordcloud.add('',data, shape = 'triangle')
### 渲染图片
mywordcloud.render('./诗词词云图.html') # render ---提交
### 指定渲染图片存放的路径