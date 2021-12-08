# -*- coding: utf-8 -*- 
# @Time : 2021/12/7 15:00 
# @Author : J.wang 
# @File : py_insert.py
'''
    # 数据插入：动态插入数据
'''
import pymysql


def insert_info(table_name, insert_columns, insert_values):
    db_inert = pymysql.Connect(host='127.0.0.1', user='root', password='159611', port=3306, database='python_mysql')
    cursor = db_inert.cursor()
    sql_insert_table = "insert into " + table_name + insert_columns + ' values ' + insert_values
    try:
        print('\033[5;30;46m\t开始插入数据 SQL \033[0m：', sql_insert_table)
        cursor.execute(sql_insert_table)
        db_inert.commit()
        print(cursor.rowcount)
    except Exception as e:
        db_inert.rollback()
        print("insert sql捕获到异常")
        raise e
    finally:
        if db_inert:
            print("关闭资源")
            cursor.close()
            db_inert.close()


def dict_column_comment_insert(create_name, table_comment, columns, dict_name):
    key_columns = columns  # 转存key
    value_columns = columns  # 转存value
    columns_v = '(' + ','.join('`' + str(column + "`") for column in key_columns.keys()) + ')'
    values_v = '(' + ','.join("'" + str(value_columns[column] + "'") for column in value_columns.keys()) + ')'
    table_name = 't_' + create_name + dict_name
    print('\033[0;33;40mtable_name:\033[0m', table_name, '\033[0;33;40m\tcolumns：\033[0m', columns_v,
          '\033[0;33;40m\tvalues：\033[0m', values_v)
    insert_info(table_name, columns_v, values_v)


# 循环解析
def fordict_insert(create_name, table_comment, for_dict, key_name):
    print('通用解析——插入数据 dict--------start--------!!!')
    if key_name != '': key_name = '_' + key_name
    dict_column_comment_insert(create_name, table_comment, for_dict, key_name)  # 组合sql
    for dd in for_dict.keys():
        table_name_last = '_' + dd
        if isinstance(for_dict[dd], dict):  # 判断是否为字典
            print('dict》》dict--------start--------')
            dict_column_comment_insert(create_name, table_comment, for_dict[dd], table_name_last)
            print(for_dict[dd])
            fordict_insert(create_name, table_comment, for_dict[dd], dd)
        elif isinstance(for_dict[dd], list):
            print('dict》》list--------start--------')
            dict_column_comment_insert(create_name, table_comment, for_dict[dd][0], table_name_last)
            fordict_insert(create_name, table_comment, for_dict[dd][0], dd)
        else:
            pass
            # print('当前不进行解析！' + dd)
            # return
    print('dict -------- end --------')


def fordata_insert(create_name, table_comment, contents):
    for key in contents.keys():
        # 判断是否为列表
        if (key == 'datas' or key == 'data') and isinstance(contents[key], list):
            fordict_insert(create_name, table_comment, contents[key][0], '')
        # 判断 是否为字典
        if (key == 'datas' or key == 'data') and isinstance(contents[key], dict):
            fordict_insert(create_name, table_comment, contents[key], '')


if __name__ == '__main__':
    body_info = {'code': '00', 'msg': '成功', 'datas': [
        {'guardian_add': '', 'address': '浙江省江山市四都镇上峰村上埂头５８号', 'guardian_name': '郑四根富',
         'pk_id': 'B9B18FCFD6B04CA6AF8C96C6E0C8C15D', 'gender': '男', 'nation': '汉族', 'birth_date': '1990-12-16',
         'disable_leve': '三级', 'disable_type': '肢体残疾', 'guardian_ide': '', 'guardian_relation': '父母',
         'identity_card': '330881199012160714', 'native_place': '浙江省江山市四都镇上峰村上埂头５８号',
         'disable_card': '33088119901216071443', 'issue_date': '2021-07-20', 'phone': '18357065836', 'name': '郑川川',
         'guardian_phone': '18357065836', 'tong_time': '2021-10-21 23:51:14.0'}], 'dataCount': 1,
                 'requestId': 'b126b1ff226d4c679de5f9f679f6a8b9'}
    table_name = '000000000000000022'
    table_comment = '测试自动建表'
    fordata_insert(table_name, table_comment, body_info)
