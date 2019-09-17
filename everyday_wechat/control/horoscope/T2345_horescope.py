#! usr/bin/env python
# -*- coding: utf-8 -*-
"""
    爬取 星座屋 星座运势
    http://tools.2345.com/naonao/
"""
import re
from functools import reduce
import requests
from bs4 import BeautifulSoup
from everyday_wechat.utils.common import SPIDER_HEADERS

__all__ = ['get_2345_horoscope', 'get_today_horoscope']


XZW_BASE_URL_TODAY = "http://tools.2345.com/naonao/"
XZW_BASE_URL_TOMORROW = " "
CONSTELLATION_DICT = {
    "白羊座": "baiyang",
    "金牛座": "jinniu",
    "双子座": "shuangzi",
    "巨蟹座": "juxie",
    "狮子座": "shizi",
    "处女座": "chunv",
    "天秤座": "tiancheng",
    "天蝎座": "tianxie",
    "射手座": "sheshou",
    "摩羯座": "moxie",
    "水瓶座": "shuiping",
    "双鱼座": "shuangyu",
}

def get_2345_horoscope(name, is_tomorrow=False):
    '''
    获取2345网(http://tools.2345.com/naonao/)的星座运势
    :param name: 星座名称
    :return:
    '''
    if not name in CONSTELLATION_DICT:
        print('星座输入有误')
        return
    try:
        if is_tomorrow :
            print('不可查询明日运势')
            return 
            
        req_url = XZW_BASE_URL_TODAY
        resp = requests.get(req_url, headers=SPIDER_HEADERS)
        if resp.status_code == 200:
            html = resp.text
            lucky_num = ""
            lucky_color = ""
            detail_horoscope = ""
            good_partner = ""
            lucky_thing = ""
            soup = BeautifulSoup(html,"html.parser")  
            day_all_constellation_info = soup.find_all('ul', class_='constellation-list')[0]
            for day_per_constellation_info in day_all_constellation_info.find_all('li'):
                if(day_per_constellation_info.find("a").get_text() == name):
                    result_str_list = day_per_constellation_info.find("div", class_="list-right").get_text().split()
                    detail_horoscope = result_str_list[0]
                    lucky_color = result_str_list[1][5:]
                    lucky_num = result_str_list[2][5:]
                    good_partner = result_str_list[3][5:]
                    lucky_thing = result_str_list[4][5:]
                    break

            if is_tomorrow:
                detail_horoscope = detail_horoscope.replace('今天', '明天')

            return_text = '{name}{_date}运势:\n【幸运颜色】{color}\n【幸运数字】{num}\n【幸运物品】{_thing}\n【契合星座】{_partner}\n【综合运势】{horoscope}'.format(
                _date='明日' if is_tomorrow else '今日',
                name=name,
                color=lucky_color,
                num=lucky_num,
                _thing=lucky_thing,
                _partner=good_partner,
                horoscope=detail_horoscope
            )
            return return_text
    except Exception as exception:
        print(str(exception))


get_today_horoscope = get_2345_horoscope

if __name__ == '__main__':
    # print (get_constellation(3, 10))
    # print(get_xzw_text("03-18"))
    is_tomorrow = False
    print(get_2345_horoscope("水瓶座", is_tomorrow))
