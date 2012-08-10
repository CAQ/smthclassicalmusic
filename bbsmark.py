# coding=utf-8

import sys, urllib
import time
from datetime import date
import random
from myauth2 import MyAuth2

randpage = random.randint(0, 69) + 1
randpost = -1
try:
    # init the auth client
    ma2 = MyAuth2(1193184550)

    # read the page and extract info
    while randpage == 3:
        randpage = random.randint(0, 69) + 1
    #randpage = 69
    wp = urllib.urlopen('http://www.newsmth.net/bbsdoc.php?board=ClassicalMusic&ftype=3&page=' + str(randpage))
    content = wp.read()
    contentutf8 = content.decode('gb2312').encode('utf-8')
    ind1 = contentutf8.index('c.o(')
    ind2 = contentutf8.rindex('c.t();')
    postscontent = contentutf8[ind1 : ind2].strip()
    posts = postscontent.split('c.o')
    postinfos = []
    msg = '[' + time.strftime('%H:%M', time.localtime(time.time())) + ']旧帖重温：'
    for apost in posts:
        if not apost.startswith('('):
            continue
        t = apost.strip()
        t = t[1 : len(t) - 2]
        index1 = t.index(',') # after id
        index2 = t.index(',', index1 + 1) # after gid
        index3 = t.index(',', index2 + 1) # after author
        index4 = t.index(',', index3 + 1) # after flag
        index5 = t.index(',', index4 + 1) # after time
        index6 = t.index(',', index5 + 1) # after title
        # the rest are: size, imported, is_tex
        id = t[0 : index1]
        gid = t[index1 + 1 : index2]
        author = t[index2 + 2 : index3 - 1]
        thetime = date.fromtimestamp(int(t[index4 + 1 : index5]))
        title = t[index5 + 2 : index6 - 2]
        postinfos.append([id, gid, author, thetime, title])
    randpost = random.randint(0, 30) + 1
    postinfo = postinfos[randpost - 1]
    thelink = 'http://www.newsmth.net/bbscon.php?bid=24&id=' + str(postinfo[0]) + '&ftype=3&num=' + str(randpage * 30 - 30 + randpost)
    msg += postinfo[2] + '于' + str(postinfo[3]) + '发表《' + postinfo[4] + '》：'
    wp1 = urllib.urlopen(thelink)
    content1 = wp1.read()
    content1utf8 = content1.decode('gb2312').encode('utf-8')
    ind11 = content1utf8.index('prints(')
    ind12 = content1utf8.index('//-->', ind11)
    maincontent = content1utf8[ind11 : ind12]
    ind13 = maincontent.index('发信站')
    ind14 = maincontent.index('\\n\\n', ind13)
    ind15 = maincontent.rindex('※')
    if maincontent.rfind('--') >= 0:
        ind15 = maincontent.rfind('--')
    maincontent = maincontent[ind14 + 2 : ind15]
    maincontent = maincontent.replace('\\n', ' ')
    maincontent = maincontent.replace('\\r', ' ')
    maincontent = maincontent.replace('  ', ' ')
    maincontent = maincontent.replace('\\/', '/')
    msg += maincontent
    if len(msg.decode('utf-8')) > 129:
        msg = msg.decode('utf-8')[0:129].encode('utf-8') # + '…'
    msg = msg + ' ' + thelink
    #print msg

    # post to weibo
    ma2.client.post.statuses__update(status=msg)
except:
    # raise
    pass
