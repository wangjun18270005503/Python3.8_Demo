# -*- coding: utf-8 -*- 
# @Project ：Git_Python3.8_Demo 
# @Time : 2021/12/14 16:17 
# @Author : J.wang 
# @Version：V 0.1 
# @File : db_demo1.py
# @Software: PyCharm
# @desc : 通过配置文件配置数据库连接信息
import pymysql


class DatabaseInit():
    def __init__(self, host, port, user, password, database, charset):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset
        self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password,
                                    database=self.database, charset=self.charset)
        self.cur = self.conn.cursor()

    def selcetDB(self, table, clonm, data):
        try:
            sql = "SELECT * FROM {0} WHERE {1} IN ('{2[0]}','{2[1]}');".format(table, clonm, data)
            print(sql)
            # data = (role01,role02)
            a = self.cur.execute(sql)
            print(a)
            res = self.cur.fetchmany(2)
            print(res)
        except pymysql.Error as e:
            raise e
            print(u'查询数据失败')

        # else :
        #     self.cur.close()
        #     self.conn.close()

    def insertDB(self, table, data):
        try:
            sql = "INSERT INTO {0}(id,`name`,role,`desc`)VALUES('%s','%s','%s','%s');".format(table)
            self.cur.execute(sql % data)
            self.conn.commit()
        except pymysql.Error as e:
            raise e
            # print(u'插入数据失败')
            # self.conn.rollback()
        else:
            print(u'插入数据库成功')
            self.cur.close()
            self.conn.close()

    def updateDB(self, table, clonm, status, weclonm, beg):
        try:
            sql = "update {0} SET {1} = '{2}' WHERE {3} = '{4}';".format(table, clonm, status, weclonm, beg)
            self.cur.execute(sql)
            self.conn.commit()
        except pymysql.Error as e:
            raise e
        else:
            print(u'更改值成功')
            self.cur.close()
            self.conn.close()

    def deleteDB(self, table, clonm, status):
        try:
            sql = " delete FROM {0} WHERE {1} ='{2}';".format(table, clonm, status)
            self.cur.execute(sql)
            self.conn.commit()
        except pymysql.Error as e:
            raise e
        else:
            print(u'删除值成功')
            self.cur.close()
            self.conn.close()


if __name__ == '__main__':
    import configparser
    confi = configparser.ConfigParser()
    confi.read('confing.ini', encoding='utf-8')
    db = DatabaseInit(confi['DEFAULT']['ip'],
                      int(confi['DEFAULT']['port']),
                      confi['DEFAULT']['user'],
                      confi['DEFAULT']['passwd'],
                      confi['DEFAULT']['database'],
                      confi['DEFAULT']['charset'])
    data00 = ('1', '2')  #参数
    table = 't_000000000000000022' #查询库表
    clonm = 'id' #条件字段
    db.selcetDB(table, clonm, data00)
