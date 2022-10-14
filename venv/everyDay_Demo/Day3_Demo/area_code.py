# -*- coding: utf-8 -*- 
# @Project ：Git_Python3.8_Demo 
# @Time : 2022/1/18 14:32 
# @Author : J.wang 
# @Version：V 0.1 
# @File : area_code.py
# @Software: PyCharm
# @desc :
# coding=utf-8
# -*- coding: utf-8 -*-


import urllib.request
import time
from bs4 import BeautifulSoup

indexs = 'index.html'
url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2021/'
txt = urllib.request.urlopen(url + indexs).read().decode('utf8')
soup = BeautifulSoup(txt, 'html.parser')
lista = soup.find_all('a')
lista.pop()
for a in lista:
    print("========" + a['href'][0:2] + "," + a.text + "========")
    time.sleep(1)
    txt = urllib.request.urlopen(url + a['href'], timeout=5000).read().decode('utf8')
    soup = BeautifulSoup(txt, 'html.parser')
    listb = soup.find_all('a')
    listb.pop()
    bb = {}
    l = len(listb)
    # print("----->>>>> "+str(l/2)+" <<<<<<------")
    strName = ''
    for i in range(0, l - 1):
        if (listb[i].text == strName):
            continue
        strIndex = listb[i]['href']
        code = listb[i].text
        strName = name = listb[i + 1].text
        print(strIndex + "," + code + "," + name)
        time.sleep(1)
        ctxt = urllib.request.urlopen(url + strIndex, timeout=5000).read().decode('utf8')
        soup = BeautifulSoup(ctxt, 'html.parser')
        listc = soup.find_all('a')
        listc.pop()
        lc = len(listc)
        print("----->>>>> " + str(lc / 2) + " <<<<<<------")
        cstrName = ''
        for c in range(0, lc - 1):
            if (listc[c].text == cstrName):
                continue
            strIndex = listc[c]['href']
            code = listc[c].text
            cstrName = name = listc[c + 1].text
            print("   [" + code + "," + name + "]")
