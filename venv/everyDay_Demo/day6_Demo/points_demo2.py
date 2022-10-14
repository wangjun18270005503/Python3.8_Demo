# -*- coding: utf-8 -*- 
# @Project ：Git_Python3.8_Demo 
# @Time : 2022/3/31 17:36 
# @Author : J.wang 
# @Version：V 0.1 
# @File : points_demo2.py
# @Software: PyCharm
# @desc :
import json
import csv
def pointInPolygon():
    gfile = './beijing_poly_wgs84.geojson' #utf-8编码
    cin_path = './poi_cinema_wgs84.csv'
    out_path = './beijing_poi_cinema_wgs84.csv' #输出文件

    pindex = [2, 3]  # wgslng,wgslat 在的位置

    with open(out_path, 'w', newline='') as cout_file:
        fin = open(cin_path, 'r', encoding='gbk') #出现编码错误就改编码 utf-8
        gfn = open(gfile, 'r', encoding='utf-8')
        gjson = json.load(gfn)
        polygon = gjson["features"][0]["geometry"]['coordinates'] #提取多边形,如果是4维数组需要相应的处理
        filewriter = csv.writer(cout_file, delimiter=',')
        w = 0
        for line in csv.reader(fin, delimiter=','):
            if w == 0: #写入表头 id,name,… 如果没有就去掉if语句
                filewriter.writerow(line)
                w = 1
                continue
            point = [float(line[pindex[0]]), float(line[pindex][1])]
            if isPoiWithinPoly(point, polygon): #在多边形内，写入新表
                filewriter.writerow(line)
            else:
                continue
        fin.close()
        gfn.close()
    print('done')
