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
    timestr = '[' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ']'
    msg = timestr + '热门话题：'
    hashot = False
    for ahot in hots:
        if not ahot.startswith('['):
            continue
        t = ahot.strip()
        t = t[1 : len(t) - 2]
        index1 = t.index(',')
        index2 = t.rindex(',')
        postid = t[0 : index1]
        posttitle = t[index1 + 3 : index2 - 2]
        postnum = t[index2 + 2 : len(t)]
        msg += posttitle + '(' + postnum + ')' + 'http://www.newsmth.net/bbstcon.php?board=ClassicalMusic&gid=' + postid + ' '
        #print postid, posttitle, postnum
        hashot = True

    # post to weibo
    if hashot:
        ma2.client.post.statuses__update(status=msg)
    else:
        ma2.client.post.statuses__update(status='现在没有热门话题哟，快来灌水吧！ http://classicalmusic.board.newsmth.net/')
except:
    #raise
    pass
