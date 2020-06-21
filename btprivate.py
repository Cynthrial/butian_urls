#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 6/19/19 10:34 AM
# @Author  : C0nners Chan
# @File    : btprivate.py
# @Software: PyCharm
# 爬取补天私有src

import requests
from bs4 import BeautifulSoup
import sys
import threading

threadNumber = 10 # 设置线程数

def testOnline(number):
    print("############################")
    print("# " + str(number))
    url = "http://butian.360.cn/company/info/id/" + str(number)
    content = requests.get(url).text
    soup = BeautifulSoup(content, "html.parser")
    domain = soup.find("td", width="460")
    if domain != None:
        temp = domain.text
        if temp != "":
            if not (temp.startswith("http://") or temp.endswith("https://")):
                temp = "http://" + temp
            if not (temp.endswith("/")):
                temp += "/"
            _price = soup.find("td", align="center", class_="color_td3 font_width")
            if _price != None:
                price = _price.text
                print(u"# Max : " + price)
            else:
                priceTotal = "0"
            _priceTotal = soup.find("td", align="center", class_="color_td2 font_width")
            if _priceTotal != None:
                priceTotal = _priceTotal.text
                print(u"# Total : " + priceTotal)
            else:
                price = "0"
            print(temp)
            if len(price) == 1 and len(priceTotal) == 1:
                file = open("websites_free.txt","a+")
                file.write(temp + "\r\n")
                file.close()
            else:
                file = open("websites.txt","a+")
                file.write(temp + "\r\n")
                file.close()

class myThread (threading.Thread):
    def __init__(self, number):
        threading.Thread.__init__(self)
        self.number = number

    def run(self):
        testOnline(self.number)

threads = [] # 线程池

for number in range(1247,10000):
    threads.append(myThread(number))

for t in threads:
    t.start()
    while True:
        if(len(threading.enumerate())<threadNumber):
            break

