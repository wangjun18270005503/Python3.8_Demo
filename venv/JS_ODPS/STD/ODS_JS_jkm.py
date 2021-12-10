# -*- coding: utf-8 -*- 
# @Time : 2021/12/9 15:55 
# @Author : J.wang 
# @File : ODS_JS_jkm.py
import sys
from odps import ODPS
from odps.df import DataFrame
import pandas as pd
reload(sys)
sys.setdefaultencoding("utf8")

# o = ODPS("pcM6ZkvR4vULUx1x","r4PjukdD10rxDb6kyoRdzm2qQPf5HH","qz_jssjzyzx_dsj","http://service.odps.aliyun.com/api")

o = ODPS('O4iewWeaBFZdywzT', 'wG3L8OwQzENU6B5WbOYPGvkFVRKQfe',
         project='js_szhgg', endpoint='http://service.cn-qz-qzyzx-dt01.odps.qzyzx-ops.com:80/api')
js_jkm = DataFrame(o.get_table('ods_xxzhcs_js_jkm'))
print (js_jkm.head(5))