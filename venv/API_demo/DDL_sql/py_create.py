# -*- coding: utf-8 -*- 
# @Time : 2021/12/7 11:12
# @Author : J.wang
# @File : create.py

import pymysql
db = pymysql.Connect(host='127.0.0.1', user='root', password='159611', port=3306, database='python_mysql')
cursor = db.cursor()
def create_table(create_name,table_comment):
    print('开始自动建表！！！')
    try:
        cursor.execute("DROP TABLE IF EXISTS t_"+create_name)
        print(cursor.rowcount)
        column_comment = """
        `identity_card` varchar(100) NOT NULL DEFAULT '' COMMENT '',
        `name` varchar(100) NOT NULL DEFAULT '' COMMENT '',
        `input_cardId` varchar(100) NOT NULL DEFAULT '' COMMENT '',
        """
        sql_create_table = "CREATE TABLE t_"+create_name+"""
                (`id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',"""+column_comment+"""       
                `remarks` varchar(100) NOT NULL DEFAULT '' COMMENT '备注',
                `update_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '修改时间',
                `update_by` varchar(60) NOT NULL DEFAULT '1',
                `create_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                `create_by` varchar(60) NOT NULL DEFAULT '1',
                `del_flag` char(1) NOT NULL DEFAULT '0' COMMENT '0正常，1删除',
                PRIMARY KEY (`id`)
                 ) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8mb4 COMMENT='"""+table_comment+"';"
        print(sql_create_table)
        cursor.execute(sql_create_table)
        db.commit()
        print(cursor.rowcount)
    except pymysql.Error as e:
        print("数据库连接失败：" + str(e))
    finally:
        if db:
            db.close()
            cursor.close()
            print ('关闭数据库连接....')

def fordict(contents):
    for key in contents.keys():
        # 判断是否为列表
        if (key == 'datas' or key == 'data') and isinstance(contents[key], list):
            for dd in range(len(contents[key])):
                print('当中为数据判断是为列表类型的数据内容输出--------start--------')
                print(contents[key][dd])
                print('当中为数据判断是为列表类型的数据内容输出--------end--------')
                #判断是否为字典
                if isinstance(contents[key][dd], dict):
                    print('当中为数据字典值内容输出--------start--------')
                    for dict_str in (contents[key][dd]).keys():
                        # print(fordict(contents[key][dd]))
                        print('key：'+dict_str)
                        print('value：'+contents[key][dd][dict_str])
                    print('当中为数据字典值内容输出--------end--------')
                else:
                    return
        # 判断 是否为字典
        print(contents[key])
        if (key == 'datas' or key == 'data') and isinstance(contents[key], dict):
            print('dict --------start--------')
            # param_str = '{' + ",".join('"' + str(params[n] + '":"' + str(param_list[i][n]) + '"') for n in range(len(params))) + '}'
            column_str = ",".join("'"+str(dd+"' varchar(100) NOT NULL DEFAULT '' COMMENT ''") for dd in (contents[key]).keys())
            print(column_str)
            for dd in (contents[key]).keys():
                # print(dd)
                # print(contents[key][dd])
                # 判断是否为字典
                if isinstance(contents[key][dd], dict):
                    print('dict》》dict--------start--------')
                    for dict_str in (contents[key][dd]).keys():
                        # print(fordict(contents[key][dd]))
                        print('key：' + dict_str)
                        print('value：' + contents[key][dd][dict_str])
                    print('当中为数据字典值内容输出--------end--------')
                elif isinstance(contents[key][dd], list):
                    print('dict》》list--------start--------')
                    print(contents[key][dd])
                else:
                    print(dd)
                    # return
            print('当中为数据判断是为列表类型的数据内容输出--------end--------')

# 调用方法 刷新请求密钥方法
if __name__ == "__main__":
    create_name = '000000000000000022'
    table_comment = '测试自动建表'
    # str_list = {'code': '00', 'msg': '成功', 'datas': [{'guardian_add': '', 'address': '浙江省江山市廿八都镇枫岭路２号', 'guardian_name': '林秀香', 'pk_id': 'B9771869928A48499380C81378BB6D95', 'gender': '男', 'nation': '汉族', 'birth_date': '1953-02-20', 'disable_leve': '三级', 'disable_type': '肢体残疾', 'guardian_ide': '', 'guardian_relation': '其他', 'identity_card': '330823195302208913', 'native_place': '浙江省江山市廿八都镇枫岭路２号', 'disable_card': '33082319530220891343', 'issue_date': '2012-09-30', 'phone': '', 'name': '吴享根', 'guardian_phone': '', 'tong_time': '2021-10-09 03:22:49.0'}], 'dataCount': 1, 'requestId': 'b6529fe3ddca431799d9a7c72b5fa390'}
    # print(type(str_list))
    # print(type(str_list['datas']))
    # fordict(str_list)
    str_object = {'code': '00', 'msg': '成功', 'data': {'guardian_add': '', 'address': '浙江省江山市廿八都镇枫岭路２号', 'guardian_name': '林秀香', 'pk_id': 'B9771869928A48499380C81378BB6D95', 'gender': '男', 'nation': '汉族', 'birth_date': '1953-02-20', 'disable_leve': '三级', 'disable_type': '肢体残疾', 'guardian_ide': '', 'guardian_relation': '其他', 'identity_card': '330823195302208913', 'native_place': '浙江省江山市廿八都镇枫岭路２号', 'disable_card': '33082319530220891343', 'issue_date': '2012-09-30', 'phone': '', 'name': '吴享根', 'guardian_phone': '', 'tong_time': '2021-10-09 03:22:49.0','datas': [{'address': '浙江省江山市廿八都镇枫岭路２号','gender': '男', 'nation': '汉族', 'birth_date': '1953-02-20', 'disable_leve': '三级', 'disable_type': '肢体残疾','identity_card': '330823195302208913','disable_card': '33082319530220891343','phone': '', 'name': '吴享根'}]}, 'dataCount': 1, 'requestId': 'b6529fe3ddca431799d9a7c72b5fa390'}
    print(type(str_object))
    print(type(str_object['data']))
    fordict(str_object)
    # create_table(create_name, table_comment)
