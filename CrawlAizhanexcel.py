#!/usr/local/bin/python
#-*-coding:utf-8-*-
# 2015-6-26 DaoXin
import pycurl
import StringIO
import urllib
import urllib2
from random import choice
from random import uniform
import re
import sys
import string
from bs4 import BeautifulSoup
import requests
import sys
import csv
import xlrd
import xlwt
from bs4 import BeautifulSoup
import time
import json

reload(sys)
sys.setdefaultencoding('utf-8')

# useragent 列表，大家可以自行去收集。不过在本例中似乎不需要这个
AGENTS = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.120 Safari/535.2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b4pre) Gecko/20100815 Minefield/4.0b4pre",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-CN) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.1.17) Gecko/20110123 (like Firefox/3.x) SeaMonkey/2.0.12",
    "Mozilla/5.0 (Windows NT 5.2; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 SeaMonkey/2.7.1",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; zh-CN) AppleWebKit/532.8 (KHTML, like Gecko) Chrome/4.0.302.2 Safari/532.8",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; zh-CN) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.464.0 Safari/534.3",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_5; zh-CN) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.15 Safari/534.13",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.186 Safari/535.1",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/125.2 (KHTML, like Gecko) Safari/125.8",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X; fr-fr) AppleWebKit/312.5 (KHTML, like Gecko) Safari/312.3",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/418.8 (KHTML, like Gecko) Safari/419.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1 Camino/2.2.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0b6pre) Gecko/20100907 Firefox/4.0b6pre Camino/2.2a1pre",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.4 (KHTML like Gecko) Chrome/22.0.1229.79 Safari/537.4",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2; rv:10.0.1) Gecko/20100101 Firefox/10.0.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:16.0) Gecko/20120813 Firefox/16.0",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X; zh-CN) AppleWebKit/528.16 (KHTML, like Gecko, Safari/528.16) OmniWeb/v622.8.0.112941",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_6; zh-CN) AppleWebKit/528.16 (KHTML, like Gecko, Safari/528.16) OmniWeb/v622.8.0",
]

# proxynum = 25
# url = "http://127.0.0.1:8000/?types=1&count=%s&protocol=0" % proxynum
# proxydict = {}
# proxylist = []
# httplist = []
# res = requests.get(
#     url)
# # print res.text
# ddata = json.loads(res.text)
# # print "http://%s:%s" % (ddata[1][0], ddata[1][1])
# for i in range(0, proxynum):
#     # print "http://%s:%s" % (ddata[i][0], ddata[i][1])
#     proxylist.append("http://%s:%s" % (ddata[i][0], ddata[i][1]))
#     proxydict['http'] = choice(proxylist)


# print proxydict

zqym = "www.zxzhijia.com"
zqymmulu = ""

class CrawlAizhanword:

    def __init__(self):
        self.UserAgent = choice(AGENTS)
        self.host = 'localhost'
        self.user = 'root'
        self.passwd = 'mysqlmm'
        # self.proxies = proxydict
        self.port = 3306
        self.db = 'aizhan'
        # self.proxies = choice(proxylist)
        self.payload = {
            "Host": "baidurank.aizhan.com",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": self.UserAgent
        }

    def htmlrequests(self, url):
        while 1:
            response = requests.get(
                url=url, headers=self.payload)
            if '您的查询太频繁了' in response.text:
                print '您的查询太频繁了'
                time.sleep(uniform(100, 200))
                continue
            else:
                # print response.text
                return response.text

    def connDb(self):
        global cur
        conn = MySQLdb.connect(host=self.host, user=self.user,
                               passwd=self.passwd, db=self.db, port=self.port, charset='utf8')
        cur = conn.cursor()
        return cur

    def Aizhangjc(self, url, zqmulu, rankpages, pages):
        keyword_data = []
        wholeindexinfo_data = []
        includenum_data = []
        chinazdict = {}
        urlzzindex = "http://baidurank.aizhan.com/baidu/%s/%s/%s/%s/" % (
            url, zqmulu, rankpages, pages)
        print urlzzindex
        urlzzindexhtml = self.htmlrequests(urlzzindex)
        soup = BeautifulSoup(urlzzindexhtml, "lxml")
        keywordulhtml = soup.select(
            ".word_record tbody tr")

        for keywordul in keywordulhtml:
            keywordinfohtml = keywordul.select(".word a")
            wholeindexinfohtml = keywordul.select("td .zhishu")
            includenumhtml = keywordul.select("td .word_record_zs")
            for wholeindexinfo in wholeindexinfohtml:
                wholeindexinfo_data.append(wholeindexinfo.string)
            for includenum in includenumhtml:
                includenum_data.append(includenum.string)
            for keywordinfo in keywordinfohtml:
                keyword_data.append(keywordinfo.string.strip())
        chinazdict = {'keyword': keyword_data,
                      'includenum': includenum_data, 'wholeindex': wholeindexinfo_data}
        return chinazdict


# CrawlAizhanword = CrawlAizhanword()
# print CrawlAizhanword.Aizhangjc("info.gongchang.com", 1)
CrawlAizhanword = CrawlAizhanword()
# pagenum = CrawlAizhanword.Aizhangjc("www.pchouse.com.cn", 1, 1)
# print pagenum
keywordlistzz = []
includenumlistzz = []
wholeindexlistzz = []


# mysqltable="aizhan_1688chanpin_keyword"
for ranknum in range(1, 6):
    for num in range(1, 40):
        aizhangjcdict = CrawlAizhanword.Aizhangjc(
            zqym, zqmulu=zqymmulu, rankpages=ranknum, pages=num)
        keywordlist = aizhangjcdict['keyword']
        keywordlistzz.extend(keywordlist)
        includenumlist = aizhangjcdict['includenum']
        includenumlistzz.extend(includenumlist)
        wholeindexlist = aizhangjcdict['wholeindex']
        wholeindexlistzz.extend(wholeindexlist)
        time.sleep(uniform(5, 12))
# try:

#     conn = MySQLdb.connect(host='localhost', user='root',
#                            passwd='mysqlmm', db='aizhan', port=3306, charset='utf8')
#     cur = conn.cursor()
#     conn.select_db('aizhan')
#     cur.execute('CREATE TABLE %s(keyword varchar(200),includenum int(30),wholeindex int(10)) ENGINE = MyISAM DEFAULT CHARSET = utf8'%mysqltable)
#     params = [(keywordlistzz[i],includenumlistzz[i],wholeindexlistzz[i]) for i in xrange(len(keywordlistzz))]
#     cur.executemany('insert into {0}(keyword,includenum,wholeindex) values(%s,%s,%s)'.format(mysqltable), params)
#     conn.commit()
#     cur.close()
#     conn.close()

# except MySQLdb.Error, e:
#     print "Mysql Error %d: %s" % (e.args[0], e.args[1])

# 创建工作簿
f = xlwt.Workbook()
# 创建一个 user_info 的 sheet
sheet1 = f.add_sheet(u'keyword_info', cell_overwrite_ok=True)

for i in xrange(len(keywordlistzz)):
    sheet1.write(i, 0, keywordlistzz[i])
    sheet1.write(i, 1, includenumlistzz[i])
    sheet1.write(i, 2, wholeindexlistzz[i])

f.save('%s.xls' % zqym)
