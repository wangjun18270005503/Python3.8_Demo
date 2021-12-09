# -*- coding: utf-8 -*- 
# @Time : 2021/12/9 10:06 
# @Author : J.wang 
# @File : thread_demo2.py


import flask
from flask import jsonify
from flask import request

from gevent import pywsgi

import sys
reload(sys)
import time
sys.setdefaultencoding('utf-8')

server = flask.Flask(__name__)

import threading
import time

exitFlag = 0

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter, app_id):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.app_id = app_id
    def run(self):
        print ("开始线程：" + self.name)
        print_time(self.name, self.counter, 1, self.app_id)
        print ("退出线程：" + self.name)

def print_time(threadName, delay, counter, app_id):
    while counter:
        if exitFlag:
            threadName.exit()
        time.sleep(delay)
        print ("%s: %s" % (threadName, time.ctime(time.time())))
        dowork(app_id)
        counter -= 1

@server.route('/register', methods=['get', 'post'])
def registerPost():
    # post请求获取请求的参数，返回结果类型是str
    username = request.values.get('username')
    pwd = request.values.get('pwd')
    app_id = request.values.get('app_id')

    # 创建新线程
    thread1 = myThread(1, "Thread-1", 1, app_id)
    # 开启新线程
    thread1.start()

    # confirmpwd = request.values.get('confirmpwd')
    if username and pwd:  # 判断输入的用户名、密码、确认密码都不为空
        return ("用户名为：%s, 密码为：%s" % (username, pwd))
    else:
        return jsonify({"code": 504, "msg": "必填项不能为空"})


if __name__ == '__main__':
    # port可以指定端口，默认端口是5000
    # host默认是127.0.0.1,写成0.0.0.0的话，其他人可以访问，代表监听多块网卡上面，
    # server.run(debug=True, port=9898, host='0.0.0.0')
    server = pywsgi.WSGIServer(('0.0.0.0', 9898), server)
    server.serve_forever()