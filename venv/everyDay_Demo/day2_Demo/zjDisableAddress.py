#!/usr/bin/python
import mysql.connector
import requests
import json
import traceback
import redis
import re


# 浙江省残联残疾人详细地址空间地理信息获取


# 初始化数据库连接参数
mydb = mysql.connector.connect(
    # host="223.4.74.187",
    # port=3306,
    # user="libinbin@scl_pre@172.31.60.215",
    # password="kaoshi990",
    # database="provincial_szhgg_charts_pre"
    host="223.4.74.187",
    port=3306,
    user="libinbin@scl_test@172.31.60.215",
    password="kaoshi990",
    database="provincial_szhgg_charts_test",
    # host="127.0.0.1",
    # user="root",
    # password="123456",
    # auth_plugin="mysql_native_password",
    # port=3306,
    # database="provincial_szhgg_charts_pre"
)


# conn = Redis()
#连接对象
# redisPool = redis.ConnectionPool(host='localhost',port=6379,db=4,max_connections=100)
redisPool = redis.ConnectionPool(host='192.168.110.242',port=6379,db=4,max_connections=100)
redisConn = redis.Redis(connection_pool=redisPool)


# 请求获取token
def __requestGetToken__():
    token = ''
    url = "http://59.202.42.155:6107/dataDocking/api/jwtToken?appSecret=229b07099a0247a4a1cea5f3c3ef9543&appKey=8094670f5fd2483a"
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    if response != None:
        responseJson = response.json()
        if responseJson['code'] == '200':
            token = responseJson['data']
            redisConn.set('token', token, ex=1800)
    return token


# 全角数字转换为半角数字
def __FullAngleTrun__(address):
    fullAngle = {"０":"0","１":"1","２":"2","３":"3","４":"4","５":"5","６":"6","７":"7","８":"8","９":"9","－":"-","（":"(","）":")","Ａ":"A","Ｂ":"B","Ｃ":"C","Ｄ":"D","Ｅ":"E","Ｆ":"F","Ｇ":"G","Ｈ":"H","Ｉ":"I","Ｊ":"J","Ｋ":"K","Ｌ":"L","Ｍ":"M","Ｎ":"N","Ｏ":"O","Ｐ":"P","Ｑ":"Q","Ｒ":"R","Ｓ":"S","Ｔ":"T","Ｕ":"U","Ｖ":"V","Ｗ":"W","Ｘ":"X","Ｙ":"Y","Ｚ":"Z"}
    for key in fullAngle.keys():
        if(address.find(key)>=0):
            address = address.replace(key, fullAngle.get(key))
    return address

# 转换各街道下级乡村名称为映射名称
# exp: 陈村村西垄  -> 陈村村西垄自然村
def __countyMapping__(streetAreaCode, address):
    sql_enum_countyname = "select street_area_code,dp_county_name,enum_county_name from enum_countyname_mapping where del_flag = '0' and street_area_code = "
    enumCountyNameCursor = mydb.cursor()
    enumCountyNameCursor.execute(sql_enum_countyname + "\"" + streetAreaCode.__str__() + "\"")
    dbdata = enumCountyNameCursor.fetchall()
    dpCountyName = ''
    enumCountyName = ''
    for countyMapping in dbdata:
        dpCountyName = countyMapping[1]
        enumCountyName = countyMapping[2]
        if(address.find(enumCountyName) >=0):
            return address
        elif address.find(dpCountyName) >=0:
            return address.replace(dpCountyName, enumCountyName)
    return address


# 将有102幢405室这种数据设置为102幢, １６幢４单元４０２室
# 去除最后为室的那部分数据，去除最后()部分数据。
def __addressDelRoom__(orgAddress):
    address = orgAddress
    # 截取存在特殊字符的数据
    if(address.rfind("]") >= 0):
        if(len(address) == address.rindex("]") + 1):
            address = address.encode('utf-8').decode('utf-8')[0:address.rindex("]")]
    if(address.rfind("{") >= 0):
        if(len(address) == address.rindex("{") + 1):
            address = address.encode('utf-8').decode('utf-8')[0:address.rindex("{")]
    if(address.rfind("}") >= 0):
        if(len(address) == address.rindex("}") + 1):
            address = address.encode('utf-8').decode('utf-8')[0:address.rindex("}")]
    # 删除最后有括号的
    if(address.find("(") >= 0):
        address = address.encode('utf-8').decode('utf-8')[0:address.index("(")]
    if(address.find(" ") >= 0):
        address = address.encode('utf-8').decode('utf-8')[0:address.index(" ")]
    if(address.rfind("室") >= 0):
        if(len(address) == address.rindex("室") + 1):
            address = address.encode('utf-8').decode('utf-8')[0:address.rindex("室")]
    if(address.rfind("-") >= 0):
        if(len(address) == address.rindex("-") + 1):
            address = address.encode('utf-8').decode('utf-8')[0:address.rindex("-")]
    if(address.rfind("、") >= 0):
        if(len(address) == address.rindex("、") + 1):
            address = address.encode('utf-8').decode('utf-8')[0:address.rindex("、")]
    # 查找最后几个字符是数字的，删除数字部分
    r = re.search('\d+$',address)
    if r:
        address = address.encode('utf-8').decode('utf-8')[0:address.index(r.group())]
    if(address != orgAddress):
        address = __addressDelRoom__(address)    
    return address

# 替换多余数据
def __addressReplaceSurplus__(address):
    if(address.find(".")):
        address = address.replace(".","")
    return address


# "浙江省江山市双塔街道江滨四区１０２幢三单元４０５室"截取后为"江滨四区１０２幢三单元４０５室"
# 截取地址街道后详细地址
def __getStreetDetailAddress(area, address):
    sql_enum_area = "select enum_value,parent_enum_value,enum_name,enum_level,area_code,lat,lot from enum_area where del_flag = '0' AND enum_value = "
    enumAreaCursor = mydb.cursor()
    enumAreaCursor.execute(sql_enum_area + "\"" + area.__str__() + "\" limit 1 ")
    dbdata = enumAreaCursor.fetchall()
    parentEnumValue = ''
    addressMatch = ''
    for addressDbdata in dbdata:
        parentEnumValue = addressDbdata[1]
        if address.find(addressDbdata[2].decode()) >= 0:
            addressMatch = addressDbdata[2].decode()
            # parentEnumValue = addressDbdata[1]
            # if(parentEnumValue != None):
            #     address = __getStreetDetailAddress(parentEnumValue, address)
            # if(address.startswith(addressDbdata[2].decode())):
            #     address = address[len(addressDbdata[2].decode()):len(address)+1]
    if(parentEnumValue != None):
        address = __getStreetDetailAddress(parentEnumValue, address)
    if(address.startswith(addressMatch)):
            address = address[len(addressMatch):len(address)+1]
    return address

# 处理详细住址信息
def __getAddress__(areaCode,enumValue, houseAddress):
    address = ''
    # 替换多余数据
    address = __addressReplaceSurplus__(houseAddress)
    # 地区名称映射
    address = __countyMapping__(areaCode, address)
    # 截取省市县街道数据
    address = __getStreetDetailAddress(enumValue, address)
    # 特殊的市区字符去除
    if(address.startswith("市区")):
        address = address[len("市区"):len(address)+1]
    # 全角数字转换为半角数字
    address = __FullAngleTrun__(address)
    # 删除尾部房间等无关信息
    address = __addressDelRoom__(address)
    # print("街道下详细地址:%s" %address)
    return address

# 元组比较为空返回false
def compare_empty(tuple):
    if tuple == []:
        return False
    elif(tuple == '[]'):
        return False
    return True



# 组装url请求参数
# ?page=1&pageSize=10&enumValue=330822002&appKey=a200d212-57cb-11ec-9a32-00163e01215b&address=詹家山村芳树底10号
def __urlParamsPackage__(areaCode,appKey,address):
    paramStr = '?'
    params = dict()
    tup1 = ('page', 'pageSize', 'enumValue', 'appKey','address')
    # 默认为返回一条
    params['page'] = 1
    params['pageSize'] = 1
    params['enumValue'] = areaCode
    params['appKey'] = appKey
    params['address'] = address
    pi=0
    print("请求参数：", end="")
    while pi < len(tup1):
        paramStr = paramStr + tup1[pi] + '=' + str(params[tup1[pi]]) + '&'
        print("%s : %s," %(tup1[pi],params[tup1[pi]]), end="")
        pi+=1
    # print("参数组装完成，开始请求接口！")
    paramStr = paramStr.rstrip('&')
    return paramStr

# 获取token
def __getToken__():
    result = redisConn.get('token')
    if result == None:
        result = __requestGetToken__()
    else:
        result = result.decode('utf-8')
    return result

# 刷新token
def __refreshToken__():
    __requestGetToken__()



# 模糊查询已定位地址名称
def __fuzzyQuery__(areaCode, address):
    url_param_appKey = "a200d212-57cb-11ec-9a32-00163e01215b"
    url = "http://59.202.42.155:6107/dataDocking/api//address/positionAddress"
    pageSize = 1
    paramStr = __urlParamsPackage__(areaCode, url_param_appKey, address)
    payload = {}
    backResponse = None
    headers = {'token': __getToken__()}
    url += paramStr
    if(address.strip() != ''):
        # ?page=1&pageSize=1&enumValue=330822002&appKey=a200d212-57cb-11ec-9a32-00163e01215b&address=詹家山村芳树底10号
        r = requests.request("GET", url, headers=headers, data=payload)
        # print(r.json())
        backResponse = r.json()
    return backResponse


def disableHouseAddress(area,limit_size,customPage):
    # 数据库查询sql
    # 查询总的数量
    sql_find_count = "SELECT count( 1 ) AS count FROM dp_info AS ds LEFT JOIN enum_area AS t ON t.area_code_sub = ds.area_code_sub AND t.enum_name = ds.street LEFT JOIN enum_disable_area_info AS ed ON ed.dp_id = ds.id WHERE ds.del_flag = '0' AND ds.`status` = '持证' AND t.del_flag = '0' AND ed.id IS NULL and ds.area_code like '" + area + "%' AND t.area_code LIKE '" + area + "%'"

    # 查询详细数据
    # sql_find_area = "SELECT ds.`name`,ds.street,ds.id_card,ds.household_address, t.area_code,t.enum_value,dp.id FROM dp_statistics_info AS ds LEFT JOIN enum_area AS t ON t.enum_name = ds.street left join enum_disable_area_info as ed on ed.id_card = ds.id_card WHERE ds.del_flag = '0' and ds.`status` = '持证' AND t.del_flag = '0' and ed.id is null and t.area_code like '3308%' ORDER BY ds.create_date asc "
    sql_find_area = "SELECT ds.`name`,ds.street,ds.id_card,ds.undes_household_address,t.area_code,t.enum_value,ds.id,ds.street_area_code FROM dp_info AS ds LEFT JOIN enum_area AS t ON t.area_code_sub =  ds.area_code_sub and t.enum_name = ds.street LEFT JOIN enum_disable_area_info AS ed ON ed.dp_id = ds.id WHERE ds.del_flag = '0' AND ds.`status` = '持证' AND t.del_flag = '0' AND ed.id IS NULL and t.enum_level = '3'AND t.area_code LIKE '" + area + "%' and ds.area_code like '" + area + "%' ORDER BY ds.create_date ASC "

    # 插入数据库
    sql_insert_disable_area = "insert into enum_disable_area_info(id_card,name,area_code,address,lat,lon,house_address,street, back_address,dp_id, create_date,back_info) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now(),%s);"

    # 查询总条数
    conn = mydb.cursor()
    conn.execute(sql_find_count)
    alldata = conn.fetchall()
    count = 0
    for c in alldata:
        count = c[0]
        print("count:%s" %(count))
    page = count / limit_size
    print("++++++++++++++++++++++++++page:%i" %page)
    # 循环page+1次查询数据，分页limit_size
    #  用于测试，设置指定的page
    if customPage != 0:
        page = customPage
    i = 0
    while i <= page:
        print("+++++++++++++++++++++++")
        sqlconn = mydb.cursor()
        sqlconn.execute(sql_find_area + " limit " + limit_size.__str__())
        dbdata = sqlconn.fetchall()
        insertValues = list()
        j=0
        for singleDbData in dbdata:
            j+=1
            # 对每一条数据进行处理
            # print("name:%s, street:%s,idCard:%s,house_address:%s,area_code:%s" %(singleDbData[0], singleDbData[1].decode("UTF-8"), singleDbData[2], singleDbData[3],singleDbData[4]))
            name = singleDbData[0]
            street = singleDbData[1].decode()
            idCard = singleDbData[2]
            houseAddress = singleDbData[3]
            areaCode = singleDbData[4]
            enumValue = singleDbData[5]
            dpId = singleDbData[6]
            # "浙江省江山市市区江滨新村１幢２０２室" 转换为 "江滨新村1幢"
            lon = '0'
            lat = '0'
            backAddress = ''
            address = ''
            backInfo = ''
            try:
                address = __getAddress__(areaCode, enumValue, houseAddress)
            except:
                traceback.print_exc()
                backInfo = '地址信息处理异常，未请求！'
                print('第%s条，%s地址信息处理异常。' %(j,houseAddress))
                data_disable=(idCard,name,areaCode,address,lat,lon,houseAddress,street,backAddress,dpId,backInfo)
                insertValues.append(data_disable)
                continue
            if address == '不详' or address == '':
                print('第%s条，%s地址信息处理异常。' %(j,houseAddress))
                data_disable=(idCard,name,areaCode,address,lat,lon,houseAddress,street,backAddress,dpId,backInfo)
                insertValues.append(data_disable)
                continue
            # houseAddress = ''
            # 请求request获取空间地理信息，请求参数：page,pageSize,enumValue,appKey,houseAddress,enumValue
            backResponse = __fuzzyQuery__(areaCode, address)
            # 处理url请求返回的数据
            try:
                backInfo = json.dumps(backResponse,ensure_ascii=False)
                if(backResponse != None):
                    if(backResponse['code'] != None and backResponse['code'] == '200' and backResponse['msg']=='请求成功'):
                        if(compare_empty(backResponse['data'])):
                            baskData = backResponse['data']
                            # print(baskData)
                            # [{BZ_ADDRESS_UUID='', ENTI_CODE='', XZQHDM='86330881110', PROVINCE='浙江省', CITY='衢州市', COUNTY='江山市', EXCLUSIVEZONE='', TOWN='凤林镇', ADDRESS='凤翔路108号', LON='118.4910980612', LAT='28.5238069296', DATA_VERSION='', CHECK_UNIT='', STATE='有效', LEGAL_STATUS='法定数据', UPDATETIME='2019-10-02 10:39:37.0', REMARK='原门牌证号:0'}]
                            dataList = baskData.replace("='", "\":\"").replace("[{", "[{\"").replace("', ", "\",\"").replace("'}]", "\"}]").replace("}, {", "\"}, {\"").replace("\n", "").replace("\t","").replace("\r","")
                            recordList = json.loads(dataList)
                            # print(recordList)
                            record = recordList[0]
                            # print(record)
                            lon = record['LON']
                            lat = record['LAT']
                            backAddress = record['ADDRESS']
                # 插入表中，字段有id_card,name,area_code,address,lat,lot
                data_disable=(idCard,name,areaCode,address,lat,lon,houseAddress,street,backAddress,dpId,backInfo)
                print("第%s条，待插入数据：%s" %(j,(data_disable[0:len(data_disable)])))
                insertValues.append(data_disable)
            # except EOFError():
            #     print("处理url返回数据异常。")
            #     pass
            # except Exception(e):
            #     print("处理url异常:%s" %e)
            except:
                print("异常信息")
                traceback.print_exc()
                __refreshToken__()
                break
            # else:
            #     print("处理url异常。")
        
        # 批量插入数据库提高效率
        try:
            insertCursor = mydb.cursor()
            # print(insertValues)
            insertCursor.executemany(sql_insert_disable_area,insertValues)
            mydb.commit()
        except Exception():
            raise Exception("批量插入数据异常", insertCursor)
            pass
        i+=1

# 浙江省城市循环数据进行处理
def cycleCityWithSize(countyCode, cityCount, cycle, limit_size, customPage):
    # 默认limit_size为数据库查询的数据量，可以设置为500
    # customPage用于测试设置循环request请求次数默认为0则是根据数据库查询数据量自动计算
    zjAreaCode = countyCode
    # 循环多个城市
    if(cycle == True):
        i = 1
        print("cycle city cityCount:%s" %cityCount)
        for i in range(1, cityCount+1):
            cityAreaCode = zjAreaCode
            if(i>9):
                cityAreaCode += i.__str__()
            else:
                cityAreaCode = cityAreaCode + "0" + i.__str__()
            print("开始进行城市编码为：%s的城市开始匹配数据." %cityAreaCode)
            disableHouseAddress(cityAreaCode, limit_size, customPage)
    else:
        # 非循环，只查当前城市数据
        i=cityCount
        print("city :%s" %i)
        cityAreaCode = zjAreaCode
        if(cityCount >9):
            cityAreaCode += i.__str__()
        else:
            cityAreaCode = cityAreaCode + '0' + i.__str__()
        disableHouseAddress(cityAreaCode, limit_size, customPage)

def cycleCity(countyCode, cityCount, cycle):
    limit_size = 500
    customPage = 0
    cycleCityWithSize(countyCode, cityCount, cycle, limit_size,customPage)

# 浙江省编码开头为33，总共有11个城市
# countyCode = '33'
# cityCount = 1
# cycleCity(countyCode, cityCount, False)


# 设置区域参数，从enum_area表中获取区县市的enum_value
# areaCode = "3304"
# enumValue = '86330402007'
# houseAddress = "浙江省嘉兴市南湖区少年公寓１幢５０３室（编号：1010255）"
# address = __getAddress__(areaCode, enumValue, houseAddress)

# areaName = ''
# __getFullEnumValue__(area, areaName)
# address = '浙江省江山市凤林镇官田村黄柿坞３４号'
# address = __getStreetDetailAddress(area, address)
# print(address)

