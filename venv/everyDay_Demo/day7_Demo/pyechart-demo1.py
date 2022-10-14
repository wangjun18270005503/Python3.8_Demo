# -*- coding: utf-8 -*- 
# @Project ：pythonProject2 
# @Time : 2022/5/25 11:40 
# @Author : J.wang 
# @Version：V 0.1 
# @File : pyechart-demo1.py
# @Software: PyCharm
# @desc :  python 调用echart 交互式可视化  Bar(柱状图/条形图)


import pandas as pd
from pyecharts.charts import Bar
from pyecharts import options as opts
# 内置主题类型可查看 pyecharts.globals.ThemeType
from pyecharts.globals import ThemeType

if __name__ == "__main__":
    data = pd.read_excel("./data/全国市县街道数量分布.xlsx", header=None)
    df_li = data.values.tolist()
    x = []
    y1 = []
    y2 = []
    y3 = []
    del (df_li[0])
    for s_li in df_li:
        print(s_li)
        x.append(s_li[0])
        y1.append(s_li[1])
        y2.append(s_li[2])
        y3.append(s_li[3])
    bar = (  # 图表风格 CHALK、DARK
        Bar(init_opts=opts.InitOpts(theme=ThemeType.DARK))
            .add_xaxis(x)
            .add_yaxis("市（数量）", y1)
            .add_yaxis("县（数量）", y2)
            .add_yaxis("街道（数量）", y3)
            .set_global_opts(init_opts=opts.InitOpts(width="1600px", height="1000px"),
                             title_opts=opts.TitleOpts(title="全国各省份下级单位数量", subtitle="个"),
                             datazoom_opts=opts.DataZoomOpts(is_show=True))
    )
    # bar.add('房屋均价',x,y1,mark_point=["max","min"],mark_line=["average"],is_label_show=True)
    # bar.add('人均工资', x, y2,is_datazoom_show=True)
    bar.render('./data/条形图02.html')
