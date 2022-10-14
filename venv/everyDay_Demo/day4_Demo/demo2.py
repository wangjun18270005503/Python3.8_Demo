# -*- coding: utf-8 -*- 
# @Project ：Git_Python3.8_Demo 
# @Time : 2022/3/3 16:28 
# @Author : J.wang 
# @Version：V 0.1 
# @File : demo2.py
# @Software: PyCharm
# @desc : https://www.cnblogs.com/CoffeeSoul/p/13026274.html
from pyecharts import options as opts
from pyecharts.charts import Page, WordCloud
from pyecharts.globals import SymbolType


words = [
("手中雕刻生花", 10000),
("刀锋千转蜿蜒成画", 6181),
("盛名功德塔", 4386),
("是桥畔某处人家", 4055),
("春风绕过发梢红纱", 2467),
("刺绣赠他", 2244),
("眉目刚烈拟作妆嫁", 1868),
("轰烈流沙枕上白发", 1484),
("杯中酒比划", 1112),
("年少风雅鲜衣怒马", 865),
("也不过一刹那", 847),
("难免疏漏儿时檐下", 582),
("莫测变化", 555),
("隔却山海", 550),
("转身从容煎茶", 462),
]

worldcloud=(
WordCloud()
.add("", words, word_size_range=[20, 150])
.set_global_opts(title_opts=opts.TitleOpts(title="WordCloud-基本示例"))
)
worldcloud.render('./歌词词云图.html')