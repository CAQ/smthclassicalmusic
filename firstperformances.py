# -*- coding: utf-8 -*-

import urllib, urllib2
import cookielib
import time

def postit(title, content):
    # print title, content.replace('\\n', '\n')
    post_data = urllib.urlencode({'subject': title, 'content': content.replace('\\n', '\n')})
    req = urllib2.Request('http://m.newsmth.net/article/ClassicalMusic/post', post_data)
    urllib2.urlopen(req)
    # time.sleep(30)

today = time.localtime(time.time())
year = today.tm_year
month = today.tm_mon
day = today.tm_mday
todaystr = ('0' if month < 10 else '') + str(month) + ('0' if day < 10 else '') + str(day)

fps = []

f = open('fetchhistory/events.txt')
for line in f.readlines():
    fields = line.strip().split('\t')
    # date, year, type, details, imgs
    if len(fields) <= 1:
        continue
    if fields[0] == todaystr and fields[2] == 'FP':
        fps.append(fields)
f.close()

f = open('smthcm.config')
usrpwd = f.readline().strip().split('\t')
f.close()
post_data = urllib.urlencode({'id': usrpwd[0], 'passwd': usrpwd[1]})
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0'), ('Referer', 'http://m.newsmth.net/'), ('Host', 'm.newsmth.net')]
urllib2.install_opener(opener)
req = urllib2.Request('http://m.newsmth.net/user/login', post_data)
conn = urllib2.urlopen(req)

fulltitle = '今日历史首演（' + str(month) + '月' + str(day) + '日）'
fullcontent = ''

for fp in fps:
    # date, year, type, details, imgs
    years = year - int(fp[1])
    fullcontent += str(years) + '周年\n'
    fullcontent += fp[3] + '\n\n'

if len(fullcontent) > 0:
    fullcontent += '数据来源：http://cdexchang.blogspot.com/\n\n'
    postit(fulltitle, fullcontent)

req = urllib2.Request('http://m.newsmth.net/user/logout', post_data)
conn = urllib2.urlopen(req)

