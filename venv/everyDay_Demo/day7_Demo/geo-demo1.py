# -*- coding: utf-8 -*-
# @Project ：Git_Python3.8_Demo 
# @Time : 2022/5/29 16:22 
# @Author : J.wang 
# @Version：V 0.1 
# @File : geo-demo1.py
# @Software: PyCharm
# @desc :
from pyecharts import options as opts
from pyecharts.charts import Geo
from pyecharts.globals import ChartType, SymbolType

c = (
    Geo()
    .add_schema(
        maptype="china",
        itemstyle_opts=opts.ItemStyleOpts(color="#323c48", border_color="#111"),
    )
    .add(
        "",
        [("江山", 55), ("北京", 66), ("杭州", 77), ("重庆", 88),('江西',100),('广西',100),('台湾',121),('武汉',53),('山东',53),('山西',53),('新疆',53)],
        type_=ChartType.EFFECT_SCATTER,
        color="white",
    )
    .add(
        "geo",
        [("江山", "上海"), ("江山", "北京"), ("江山", "杭州"), ("江山", "重庆"),("江西","江山"),("台湾","江山"),("武汉","江山"),("广西","江山"),("山东","江山"),("山西","江山"),("新疆","江山")],
        type_=ChartType.LINES,
        effect_opts=opts.EffectOpts(
            symbol=SymbolType.ARROW, symbol_size=6, color="blue"
        ),
        linestyle_opts=opts.LineStyleOpts(curve=0.2),
    )
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(title_opts=opts.TitleOpts(title="Geo-Lines-background"))
    .render("geo_lines_background.html")
)

