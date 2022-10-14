import pymysql
import xlwt
import datetime

#sx_local_govern_test
def local():
    db = pymysql.connect(host='10.27.166.210', port=3306, user='xxzhcs', password='Xxzhcs1234', db='sx_local_govern_test')
    sql = "SELECT table_name as 表名,table_rows as 表数据, table_comment as 名称 \
    FROM information_schema.tables \
    WHERE table_schema = 'sx_local_govern_test'and table_name not like '%copy%' and table_name not like '%_bak%' and table_name like '%local_%'"
    cursor = db.cursor()

    cursor.execute(sql)
    fileds = [filed[0] for filed in cursor.description]
    r = cursor.fetchall()
    # print(r)
    book = xlwt.Workbook()  # 创建一个book
    sheet = book.add_sheet('sheet1') #表头
    for col, field in enumerate(fileds):
        sheet.write(0, col, field)
    row = 1  # 行数
    for data in r:  # 控制行数
        for col, field in enumerate(data):  # 控制列数
            sheet.write(row, col, field)
        row += 1  # 行数加1
    book.save('D:\ local.xlsx')# 保存excel文件
    print("运行完成")

#jdhg_gyyq
def js():
    db = pymysql.connect(host='10.27.166.210', port=3306, user='xxzhcs', password='Xxzhcs1234', db='jdhg_gyyq')
    sql = "SELECT table_name as 表名,table_rows as 表数据, table_comment as 名称 \
    FROM information_schema.tables \
    WHERE table_schema = 'jdhg_gyyq'and table_name not like '%copy%' and table_name not like '%_bak%' and table_name like '%js_%'"
    cursor = db.cursor()
    cursor.execute(sql)
    fileds = [filed[0] for filed in cursor.description]
    r = cursor.fetchall()
    # print(r)
    book = xlwt.Workbook()  # 创建一个book
    sheet = book.add_sheet('sheet1')
    for col, field in enumerate(fileds):
        sheet.write(0, col, field)
    row = 1  # 行数
    for data in r:  # 控制行数
        for col, field in enumerate(data):  # 控制列数
            sheet.write(row, col, field)
        row += 1  # 行数加1
    book.save('D:\ js.xlsx')# 保存excel文件
    print("运行完成")

#xxzhcs
def warehouse():
    db = pymysql.connect(host='10.27.166.210', port=3306, user='xxzhcs', password='Xxzhcs1234', db='xxzhcs')
    sql = "SELECT table_name as 表名,table_rows as 表数据, table_comment as 名称 \
    FROM information_schema.tables \
    WHERE table_schema = 'xxzhcs'and table_name not like '%copy%' and table_name not like '%_bak%' and table_name like '%warehouse_%'"
    cursor = db.cursor()
    cursor.execute(sql)
    fileds = [filed[0] for filed in cursor.description]
    r = cursor.fetchall()
    # print(r)
    book = xlwt.Workbook()  # 创建一个book
    sheet = book.add_sheet('sheet1')
    for col, field in enumerate(fileds):
        sheet.write(0, col, field)
    row = 1  # 行数
    for data in r:  # 控制行数
        for col, field in enumerate(data):  # 控制列数
            sheet.write(row, col, field)
        row += 1
    book.save('D:\ warehouse.xlsx')# 保存excel文件
    print("运行完成")
if __name__ == '__main__':
    # starttime = datetime.datetime.now()
    local()
    js()
    warehouse()
    # endtime = datetime.datetime.now()
    # sumtime = (endtime - starttime).seconds
    # print(sumtime)
