# -*- coding: utf-8 -*- 
# @Project ：Git_Python3.8_Demo 
# @Time : 2021/12/15 9:17 
# @Author : J.wang 
# @Version：V 0.1 
# @File : corn_demo1.py
# @Software: PyCharm
# @desc :
# 根据前缀插入cron表达式和对应的时间戳
curs.execute('select job_desc,schedule_conf,trigger_last_time,trigger_next_time from xxl_job.xxl_job_info_copy1')
data = curs.fetchall()
ods_count = 0
dm_count = 0
dm_minute_start = 30
dm_hour_start = 3
ods_minute_start = 10
ods_hour_start = 0
today_datetime = datetime.date.today()
tomorrow_datetime = str(today_datetime + datetime.timedelta(days=1))
today_datetime = str(today_datetime)
for i in data:
    if i[0].startswith(dm_prefix):
        # 插入cron表达式
        dm_minute_sum = dm_count / 10 * 10 + dm_minute_start
        dm_minute = dm_minute_sum - dm_minute_sum / 60 * 60
        dm_hour = dm_minute_sum / 60 + dm_hour_start
        dm_time = "0 {dm_minute} {dm_hour} * * ?".format(dm_minute=dm_minute, dm_hour=dm_hour)
        curs.execute('update xxl_job.xxl_job_info_copy1 set schedule_conf = ? where job_desc = ?', (dm_time, i[0]))
        # 插入上下次执行时间戳（毫秒级）
        today = today_datetime + " {dm_hour}:{dm_minute}:00".format(dm_minute=dm_minute, dm_hour=dm_hour)
        tomorrow = tomorrow_datetime + " {dm_hour}:{dm_minute}:00".format(dm_minute=dm_minute, dm_hour=dm_hour)
        dm_today = datetime.datetime.strptime(today, "%Y-%m-%d %H:%M:%S")
        dm_tomorrow = datetime.datetime.strptime(tomorrow, "%Y-%m-%d %H:%M:%S")
        dm_today_stamp = str(int(time.mktime(dm_today.timetuple()) * 1000.0 + dm_today.microsecond / 1000.0))
        dm_tomorrow_stamp = str(int(time.mktime(dm_tomorrow.timetuple()) * 1000.0 + dm_tomorrow.microsecond / 1000.0))
        curs.execute('update xxl_job.xxl_job_info_copy1 set trigger_last_time = ? where job_desc = ?', (dm_today_stamp, i[0]))
        curs.execute('update xxl_job.xxl_job_info_copy1 set trigger_next_time = ? where job_desc = ?', (dm_tomorrow_stamp, i[0]))
        # count+1
        dm_count = dm_count + 1