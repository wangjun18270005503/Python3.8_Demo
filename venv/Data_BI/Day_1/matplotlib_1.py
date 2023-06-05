# -*- coding: utf-8 -*- 
# @Project : Git_Python3.8_Demo 
# @Time : 2023/6/4 17:22 
# @Author : J.wang 
# @Version: V 0.1 
# @File : matplotlib_1.py
# @Software: PyCharm
# @desc : 数据展示可视化
# API: http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.plotimport matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

fig, ax = plt.subplots()

plt.subplot(4, 1, 1)
data = pd.DataFrame(np.random.randn(1000, 4), columns=['x', 'y', 'z', 't'])
index = range(len(data))

plt.plot(index, data['x'].cumsum(), label='xxx')

plt.subplot(4, 1, 2)
plt.plot(index, data.loc[:, ['x', 'y']].cumsum())


plt.subplot(4, 1, 3)
plt.plot(index, data.loc[:, ['x', 'y', 'z']].cumsum())

plt.subplot(4, 1, 4)
plt.plot(index, data.cumsum())

fig.set_size_inches(40, 32)
plt.show()