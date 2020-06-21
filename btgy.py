#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 6/19/19 10:38 AM
# @Author  : C0nners Chan
# @File    : btgy.py
# @Software: PyCharm
# 爬取补天公益src

# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Auth: Conners Chan
# TIME: 2018/9/8   14:33

import json
import requests
import time
from bs4 import BeautifulSoup
from requests.exceptions import ReadTimeout
import lxml


def spider(pcount):
    # '''
    # 爬取所有公益厂商的ID
    # 保存为gysrc_id.txt
    # :return:
    # '''
    headers = {
        'Host': 'www.butian.net',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'http://www.butian.net/Reward/pub//Message/send',
        'Cookie': 'PHPSESSID=enqo72aue45h1hbg6u3cguor62; __q__=1544692443138; test_cookie_enable=null; __guid=138613664.4415430679088757000.1544692095368.716; __DC_monitor_count=4; __DC_sid=138613664.2410675486827421000.1544692095528.0479; __DC_gid=138613664.693680020.1544692095531.1544692445689.10',
        'Connection': 'keep-alive'
    }
    for i in range(1, pcount):
        data = {
            'p': i,
            'token': ''
        }
        time.sleep(3)
        res = requests.get('http://www.butian.net/Reward/pub/Message/send', params=data, headers=headers, timeout=(4, 20))
        allResult = {}
        allResult = json.loads(res.text)
        currentPage = str(allResult['data']['current'])
        currentNum = str(len(allResult['data']['list']))
        print('正在获取第' + currentPage + '页厂商数据')
        print('本页共有' + currentNum + '条厂商')
        for num in range(int(currentNum)):
            print('厂商名字:' + allResult['data']['list'][int(num)]['company_name'] + '\t\tavatar:' + allResult \
                ['data']['list'][int(num)]['avatar'] + '\t\t厂商ID:' + allResult['data']['list'][int(num)][
                      'company_id'])
            base = 'http://www.butian.net/Loo/submit?cid='
            with open('gysrc_id.txt', 'a') as f:
                f.write(base + allResult['data']['list'][int(num)]['company_id'] + '\n')


def url():
    # '''
    # 遍历所有的ID
    # 取得对应的域名
    # 保存为target.txt
    # :return:
    # '''
    headers = {

        'Host': 'www.butian.net',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0  ',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Referer': 'https://www.butian.net/Reward/plan',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0'
    }

    cookies = {

        '__DC_monitor_count': '29',
        '__guid': '66782632.2534021926694334500.1560835589122.8506',
        '__DC_gid': '66782632.611115740.1560835589122.1560922605361.59',
        'btlc_ab7a660c7e054d9e446e06f4571ebe41': '1c6d2efdb0d9a62b23b77264b6d5512a42744a1198d5633eb7973f752fc704fa',
        'PHPSESSID': 'igaes901lfpks8fm71lqsr49r3',
        '__q__': '1560923806772',
        '__DC_sid': '66782632.3322532378039549000.1560921346741.3696'
    }
    with open('gysrc_id.txt', 'r') as f:
        for target in f.readlines():
            target = target.strip()
            try:
                get_url = requests.get(target, headers=headers, cookies=cookies, timeout=5)
                result = get_url.text
                info = BeautifulSoup(result, 'lxml')
                f_url = info.find(name='input', attrs={"name": "host"})
                name = info.find(name='input', attrs={"name": "company_name"})
                last_url = f_url.attrs['value']
                print('厂商:' + name.attrs['value'] + '\t网址:' + f_url.attrs['value'])
                with open('target.txt', 'a') as t:
                    t.write(last_url + '\n')
                time.sleep(1)
            except AttributeError as ae:
                print(ae)
                time.sleep(181)
            except ReadTimeout:
                print('timeout')
    print('The target is right!')


if __name__ == '__main__':
    # data = {
    #     's': '1',
    #     'p': '1',
    #     'token': ''
    # }
    # res = requests.post('http://www.butian.net/Reward/pub/Message/send', data=data)
    # allResult = {}
    # allResult = json.loads(res.text)
    # allPages = str(allResult['data']['count'])
    # print('共' + allPages + '页')
    # spider(int(allPages))
    url()