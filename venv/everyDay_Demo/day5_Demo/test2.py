import pymysql
import xlwt
import datetime
import pandas as pd
from sqlalchemy import create_engine
#sx_local_govern_test
def local():
    db = pymysql.connect(host='**.**.**.210', port=3306, user='x*z*x*', password='X*z*c*1234', db='sx_local_govern_test')
    sql = "SELECT table_name as table_name,'' as count, table_comment as table_comment \
    FROM information_schema.tables \
    WHERE table_schema = 'sx_local_govern_test'and table_name not like '%copy' and table_name not like '%_bak' and table_name like 'local_%' "
    cursor = db.cursor()
    cursor.execute(sql)
    r = cursor.fetchall()
    # print(r)
    book = xlwt.Workbook()  # 创建一个book
    sheet = book.add_sheet('sheet1')
    for row in r:
        table_name = row[0]
        table_comment = row[2]
        countsql = "select count(*) AS c from  %s  " % table_name
        cursor.execute(countsql)
        results = cursor.fetchone()
        # res = (results)
        print(table_name,results[0],table_comment)
        db = pd.DataFrame()
        print(db)
        db.to_excel('tt.xls')


if __name__ == '__main__':
    # starttime = datetime.datetime.now()
    local()
    # js()
    # warehouse()
    # endtime = datetime.datetime.now()
    # sumtime = (endtime - starttime).seconds
    # print(sumtime)
