# -*- coding: utf-8 -*- 
# @Time : 2021/12/7 11:12
# @Author : J.wang
# @File : create.py

import pymysql


def create_table(create_name, table_comment, column_comment):
    print('开始自动建表！！！')
    try:
        db = pymysql.Connect(host='127.0.0.1', user='root', password='159611', port=3306, database='python_mysql')
        cursor = db.cursor()
        cursor.execute("DROP TABLE IF EXISTS "+create_name)
        print(cursor.rowcount)
        # column_comment = """
        # `identity_card` varchar(100) NOT NULL DEFAULT '' COMMENT '',
        # `name` varchar(100) NOT NULL DEFAULT '' COMMENT '',
        # `input_cardId` varchar(100) NOT NULL DEFAULT '' COMMENT '',
        # """
        sql_create_table = "CREATE TABLE if not exists "+create_name+"""
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


def dict_column_comment(create_name, table_comment, columns, dict_name):
    print(type(columns))
    print(columns)
    print('dict_name：'+dict_name)
    column_str = ",".join("`"+str(column+"` varchar(100) NOT NULL DEFAULT '' COMMENT ''") for column in (columns).keys())+','
    create_name = 't_'+create_name+dict_name
    print(create_name)
    create_table(create_name, table_comment, column_str)
    return column_str

def list_column_comment(columns):
    print(type(columns))
    print(columns)
    return ",".join("'"+str(columns[i]+"' varchar(100) NOT NULL DEFAULT '' COMMENT ''") for i in range(len(columns)))

def fordict(create_name,table_comment,for_dict,key_name):
    print('通用建表 dict!!!')
    print('dict --------start--------')
    if key_name != '' : key_name =  '_'+key_name
    column_str = dict_column_comment(create_name,table_comment,for_dict,key_name)  # 组合sql
    print(column_str)
    for dd in for_dict.keys():
        table_name_last = '_'+dd
        if isinstance(for_dict[dd], dict):  # 判断是否为字典
            print('dict》》dict--------start--------')
            print(dict_column_comment(create_name,table_comment,for_dict[dd],table_name_last))
            print(for_dict[dd])
            fordict(create_name,table_comment,for_dict[dd],dd)
        elif isinstance(for_dict[dd], list):
            print('dict》》list--------start--------')
            print(dict_column_comment(create_name,table_comment,for_dict[dd][0],table_name_last))
            fordict(create_name,table_comment,for_dict[dd][0],dd)
        else:
            print('当前不进行解析！' + dd)
            # return
    print('dict -------- end --------')

def fordata(create_name,table_comment,contents):
    for key in contents.keys():
        # 判断是否为列表
        if (key == 'datas' or key == 'data') and isinstance(contents[key], list):
            fordict(create_name,table_comment,contents[key][0],'')

            # todo --------------------------------------------------------
            # print(dict_column_comment(contents[key][0]))
            # for dd in (contents[key][0]).keys():
            #     if isinstance(contents[key][0][dd],dict):
            #         print('list》》dict----------------')
            #         print(dict_column_comment(contents[key][0][dd]))
            #     elif isinstance(contents[key][0][dd],list):
            #         print('list》》list----------------')
            #         print(dict_column_comment(contents[key][0][dd][0]))
            #     else:
            #         print('当前不进行解析！'+contents[key][0][dd])
            # todo --------------------------------------------------------

        # 判断 是否为字典
        if (key == 'datas' or key == 'data') and isinstance(contents[key], dict):
            fordict(create_name,table_comment,contents[key],'')

            # todo --------------------------------------------------------
            # column_str = dict_column_comment(contents[key])  # 组合sql
            # print(column_str)
            # for dd in (contents[key]).keys():
            #     if isinstance(contents[key][dd], dict):   # 判断是否为字典
            #         print('dict》》dict----------------')
            #         print(dict_column_comment(contents[key][dd]))
            #     elif isinstance(contents[key][dd], list):
            #         print('dict》》list----------------')
            #         print(dict_column_comment(contents[key][dd][0]))
            #     else:
            #         print('当前不进行解析！' + dd)
            #         # return
            # print('dict -------- end --------')
            # todo --------------------------------------------------------

# 调用方法 刷新请求密钥方法
if __name__ == "__main__":
    create_name = '000000000000000022'
    table_comment = '测试自动建表'
    # str_list = {'code':'00','msg':'成功','datas':[{'address':'浙江省江山市廿八都镇枫岭路２号','gender':'男','nation':'汉族','birth_date':'1953-02-20','disable_leve':'三级','disable_type':'肢体残疾','disable_card':'33082319530220891343','name':'吴享根'}],'dataCount':1,'requestId':'b6529'}
    # str_list_list = {'code':'00','msg':'成功','datas':[{'address':'浙江省江山市廿八都镇枫岭路２号','gender':'男','nation':'汉族','birth_date':'1953-02-20','disable_leve':'三级','disable_type':'肢体残疾','disable_card':'33082319530220891343','name':'吴享根','guardian_list':[{'guardian_add': '浙江省江山市廿八都镇枫岭路２号','guardian_name': '林秀香','code': '330881002000'}]}],'dataCount':1,'requestId':'b6529'}
    # str_list_object = {'code':'00','msg':'成功','datas':[{'address':'浙江省江山市廿八都镇枫岭路２号','gender':'男','nation':'汉族','birth_date':'1953-02-20','disable_leve':'三级','disable_type':'肢体残疾','disable_card':'33082319530220891343','name':'吴享根','guardian':{'guardian_add': '浙江省江山市廿八都镇枫岭路２号','guardian_name': '林秀香','code': '330881002000'}}],'dataCount':1,'requestId':'b6529'}
    # print(type(str_list))
    # print(type(str_list['datas']))
    # fordata(str_list)

    str_object = {'code':'00','msg':'成功','data':{'address':'浙江省江山市廿八都镇枫岭路２号','gender':'男','nation':'汉族','birth_date':'1953-02-20','disable_leve':'三级','disable_type':'肢体残疾','disable_card':'33082319530220891343','name':'吴享根'},'dataCount':1,'requestId':'b6529'}
    str_object_list = {'code':'00','msg':'成功','data':{'address':'浙江省江山市廿八都镇枫岭路２号','gender':'男','nation':'汉族','birth_date':'1953-02-20','disable_leve':'三级','disable_type':'肢体残疾','disable_card':'33082319530220891343','name':'吴享根','guardian_list':[{'guardian_add': '浙江省江山市廿八都镇枫岭路２号','guardian_name': '林秀香','code': '330881002000'}]},'dataCount':1,'requestId':'b6529'}
    str_object_object = {'code':'00','msg':'成功','data':{'address':'浙江省江山市廿八都镇枫岭路２号','gender':'男','nation':'汉族','birth_date':'1953-02-20','disable_leve':'三级','disable_type':'肢体残疾','disable_card':'33082319530220891343','name':'吴享根','guardian':{'guardian_add': '浙江省江山市廿八都镇枫岭路２号','guardian_name': '林秀香','code': '330881002000'}},'dataCount':1,'requestId':'b6529'}
    str_object_object_object = {'code':'00','msg':'成功','data':{'address':'浙江省江山市廿八都镇枫岭路２号','gender':'男','nation':'汉族','birth_date':'1953-02-20','disable_leve':'三级','disable_type':'肢体残疾','disable_card':'33082319530220891343','name':'吴享根','sys_area_street':{'street_name': '清湖街道','street_code': '330881103000','sys_area_village':{'village_name': '蔡家村','village_code': '330881003213'}}},'dataCount':1,'requestId':'b6529'}
    print(type(str_object_object_object))
    print(type(str_object_object_object['data']))
    fordata(create_name,table_comment,str_object_object_object)
    # # create_table(create_name, table_comment)
