# coding=utf-8

import sys, urllib
import time
from myauth2 import MyAuth2

try:
    # init the auth client
    ma2 = MyAuth2(1193184550)

    # extract hot topics from the web page
    wp = urllib.urlopen('http://www.newsmth.net/bbshot.php?board=classicalmusic')
    content = wp.read()
    contentutf8 = content.decode('gb2312').encode('utf-8')
    ind1 = contentutf8.index('parent.setHots(')
    ind2 = contentutf8.index(');', ind1)
    hotcontent = contentutf8[ind1 + 16 : ind2]
    hots = hotcontent.split('\n')
    msg = '[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ']热门话题：'
    for ahot in hots:
        if ahot.startswith('['):
            t = ahot.strip()
            t = t[1 : len(t) - 2]
            index1 = t.index(',')
            index2 = t.rindex(',')
            postid = t[0 : index1]
            posttitle = t[index1 + 3 : index2 - 2]
            postnum = t[index2 + 2 : len(t)]
            msg += posttitle + '(' + postnum + ')' + 'http://www.newsmth.net/bbstcon.php?board=ClassicalMusic&gid=' + postid + ' '
            #print postid, posttitle, postnum

    # post to weibo
    ma2.client.post.statuses__update(status=msg)
except:
    raise
    # pass
