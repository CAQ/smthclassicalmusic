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

births = []
dies = []

f = open('/home/caq/smthcm/musicians.txt')
for line in f.readlines():
    fields = line.strip().split('\t')
    if len(fields) <= 1:
        continue
    if fields[0].endswith('/' + str(month) + '/' + str(day)):
        births.append(fields)
    if fields[1].endswith('/' + str(month) + '/' + str(day)):
        dies.append(fields)
f.close()

f = open('/home/caq/smthcm/smthcm.config')
f.readline()
f.readline()
usrpwd = f.readline().strip().split('\t')
f.close()
post_data = urllib.urlencode({'id': usrpwd[0], 'passwd': usrpwd[1]})
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1')]
urllib2.install_opener(opener)
req = urllib2.Request('http://m.newsmth.net/user/login', post_data)
conn = urllib2.urlopen(req)

# for bbb in births:
#     years = year - int(bbb[0][0:4])
#     title = '今天是' + bbb[2] + bbb[3] + '诞辰' + str(years) + '周年'
#     content = '转载自' + bbb[4] + '\n\n' + bbb[5]
#     postit(title, content)

# for ddd in dies:
#     years = year - int(ddd[1][0:4])
#     title = '今天是' + ddd[2] + ddd[3] + '去世' + str(years) + '周年'
#     content = '转载自' + ddd[4] + '\n\n' + ddd[5]
#     postit(title, content)

fulltitle = '今日音乐家（' + str(month) + '月' + str(day) + '日）'
fullcontent = ''

for bbb in births:
    years = year - int(bbb[0][0:4])
    fullcontent = fullcontent + bbb[2] + bbb[3] + '诞辰' + str(years) + '周年\n'
    fullcontent = fullcontent + bbb[4] + '\n\n' + bbb[5] + '\n\n\n'

for ddd in dies:
    years = year - int(ddd[1][0:4])
    fullcontent = fullcontent + ddd[2] + ddd[3] + '去世' + str(years) + '周年\n'
    fullcontent = fullcontent + ddd[4] + '\n\n' + ddd[5] + '\n\n\n'

if len(fullcontent) > 0:
    postit(fulltitle, fullcontent)
#    print fulltitle, fullcontent

req = urllib2.Request('http://m.newsmth.net/user/logout', post_data)
conn = urllib2.urlopen(req)

