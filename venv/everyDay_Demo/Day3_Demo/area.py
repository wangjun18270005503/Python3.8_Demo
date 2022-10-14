import requests
import time
import datetime
import io
from bs4 import BeautifulSoup

url_template = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/{year}/index.html'
sql_template = "INSERT INTO `{db}`.`{table}` (`area_code`, `parent_code`, `address_name`, `full_name`, `current_level`) " \
               "VALUES ('{area_code}', '{parent_code}', '{address_name}', '{full_name}', {current_level});\n"

db = 'python_mysql'
table = 'sys_address_test'
tr_classes = ['provincetr', 'citytr', 'countytr', 'towntr', 'villagetr']
output_file = 'area.sql'

ROOT_NAME = '中国'
ROOT_CODE = '1'
ROOT_PARENT = '0'

# 1-中国 2-省 3-市 4-区县 5-乡镇街道 6-村社区
MAX_LEVEL = 6


def get_response(url):
    now = int(round(time.time() * 1000))
    keep = True
    count = 0
    while keep and count < 10:
        try:
            response = requests.get(url=url, timeout=1)
            keep = False
        except Exception as e:
            count += 1
    request_time = int(round(time.time() * 1000)) - now
    return response, request_time


def append_sql(sql, area_code, parent_code, address_name, full_name, current_level, request_time):
    sql += sql_template.format(db=db, table=table, area_code=area_code, parent_code=parent_code,
                               address_name=address_name, full_name=full_name, current_level=current_level)
    print('Level: {level} CODE: {code} NAME: {name} TIME: {time}'
          .format(level=current_level, code=area_code, name=address_name, time=request_time))
    # print(sql)
    return sql


def get_area(url, level, sql, parent_code, parent_name, task=1):
    response, request_time = get_response(url)
    if response.status_code != 200:
        if level == 1:
            return response.status_code
        else:
            return 'CONNECT ERROR\n'
    elif task == 0:
        return 200
    if level == 1:
        sql = append_sql(sql, ROOT_CODE, parent_code, ROOT_NAME, ROOT_NAME, level, request_time)
        level += 1
    soup = BeautifulSoup(response.content, 'lxml')
    for tr in soup.find_all('tr'):
        if not tr.has_attr('class'):
            continue
        if [c for c in tr['class'] if c in tr_classes]:
            if 'provincetr' in tr['class']:
                for td in tr.find_all('td'):
                    a = td.find_all('a')[0]
                    href = a['href']
                    area_code = href[: href.rfind('.')] + '0000000000'
                    sql = append_sql(sql, area_code, ROOT_CODE, a.text, ROOT_NAME + a.text, level, request_time)
                    if level < MAX_LEVEL:
                        sql = get_area(url[: url.rfind('/') + 1] + href, level + 1, sql, area_code, ROOT_NAME + a.text)
            elif tr.find_all('a'):
                a_code = tr.find_all('a')[0]
                a_name = tr.find_all('a')[1]
                href = a_code['href']
                sql = append_sql(sql, a_code.text, parent_code, a_name.text, parent_name + a_name.text, level, request_time)
                if level < MAX_LEVEL:
                    sql = get_area(url[: url.rfind('/') + 1] + href, level + 1, sql, a_code.text, parent_name + a_name.text)
            else:
                tds = tr.find_all('td')
                sql = append_sql(sql, tds[0].text, parent_code, tds[-1].text, parent_name + tds[-1].text, level, request_time)
    return sql


def get_data():
    year = datetime.datetime.today().year
    while True:
        result = get_area(url_template.format(year=year), 1, '', ROOT_PARENT, '', 1)
        if isinstance(result, int):
            year -= 1
        else:
            break
        if year < 2009:
            break
    with io.open(output_file, "w", encoding='utf-8') as file:
        file.write(result)


def check_update():
    year = datetime.datetime.today().year
    while True:
        status_code = get_area(url_template.format(year=year), 1, '', ROOT_PARENT, '', 0)
        if status_code == 200:
            print('{year}年的行政区划数据已更新'.format(year=year))
            break
        else:
            print('{year}年的行政区划数据未更新'.format(year=year))
            year -= 1
        if year < 2009:
            break


# check_update()
get_data()
