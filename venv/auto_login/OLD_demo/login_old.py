# -*- coding: utf-8 -*-
# @Time : 2021/11/30 16:15
# @Author : J.wang
# @File : auto_login_1.py
'''
  本脚本实现：辅助一键式完成系统登录
'''
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
import base64, requests


class WebdriveChrome:
    def __init__(self, driver_path):
        options = webdriver.ChromeOptions()
        options.add_argument('ignore-certificate-errors')
        driver = webdriver.Chrome(executable_path=driver_path, options=options)
        self._driver = driver

    @property
    def driver(self):
        return self.driver

    def run(self, url, info):
        pass


# 配置列表
class LoginInfo:
    def __init__(self, xpath, func, val):
        self.xpath = xpath
        self.func = func
        self.val = val


# 数字化改革堡垒机——登录
# 验证码自动识别
'''
    通过 冰拓 识别
        URL：http://bingtop.com/account/login/
        username：wangjun
        password：wangjun@12138
'''
# 获取图片验证码 url


# 账号密码
szhgg_baoleiji = (
    ('//*[@id="pwd_username"]', WebElement.send_keys, 'jss-szhgg'),
    ('//*[@id="pwd_pwd"]', WebElement.send_keys, 'P@ssw0rds')
)
# 链接地址
d = {
    '数字化改革堡垒机登录': ('https://220.191.236.163:6443/', szhgg_baoleiji),
}

# driver_path='/Users/hujian/Downloads/chromedriver'

driver_path = 'C:/Users/15961/PycharmProjects/pythonProject1/venv/py_test/chromedriver_win32/chromedriver.exe'


def run(driver, url, info):
    driver.get(url)
    task = [LoginInfo(xpath, func, val) for xpath, func, val in info]
    for t in task:
        driver.implicitly_wait(3)  # 避免模拟器运行慢获取不到元素
        obj = driver.find_element_by_xpath(t.xpath)
        t.func(obj) if t.val is None else t.func(obj, t.val)


if __name__ == '__main__':

    # key = '省公共数据平台'
    # key ='衢州市公共数据平台'
    # key = '阿里云堡垒机'
    # key = '阿里云ram'
    key = '数字化改革堡垒机登录'
    try:
        # 忽略
        options = webdriver.ChromeOptions()
        options.add_argument('ignore-certificate-errors')
        options.add_argument(
            'User-Agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36')
