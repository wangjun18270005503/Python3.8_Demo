# -*- coding: utf-8 -*- 
# @Project ：Git_Python3.8_Demo 
# @Time : 2022/1/10 19:04 
# @Author : J.wang 
# @Version：V 0.1 
# @File : getimage.py
# @Software: PyCharm
# @desc :
import requests
import os

def getImage(imgUrl):
    r = requests.get(imgUrl, stream=True)
    # extension = os.path.splitext(imgUrl)[1] # 获取扩展名
    imgName = ''.join(["./image.jpeg"])
    with open(imgName, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()
        f.close()

    return imgName


def showImage():
    image = getImage("https://yknaes.wsjkw.zj.gov.cn:16659/api/user/GetCapture?id=123737.84126937944")
    from PIL import Image
    import matplotlib.pyplot as plt
    img = Image.open(image)
    plt.figure("img")
    plt.imshow(img)
    plt.show()

if __name__ == "__main__":
    showImage()