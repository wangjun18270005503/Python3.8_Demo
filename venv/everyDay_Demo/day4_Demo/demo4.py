# -*- coding: utf-8 -*- 
# @Project ：Git_Python3.8_Demo 
# @Time : 2022/3/3 16:49 
# @Author : J.wang 
# @Version：V 0.1 
# @File : demo4.py
# @Software: PyCharm
# @desc :
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.faker import Faker
import random

days_attrs = ["{}天".format(i) for i in range(10)]
print(days_attrs)
days_values = [random.randint(1, 300) for _ in range(10)]
print(days_values)

c = (
    Bar()
    .add_xaxis(days_attrs)
    .add_yaxis("各类型残疾人情况", days_values)
    .set_global_opts(
        title_opts=opts.TitleOpts(title="Bar-DataZoom（slider-水平）"),
        datazoom_opts=opts.DataZoomOpts(),
    )
    .render("bar_datazoom_slider.html")
)