# coding=utf-8

import sys, urllib
from weibopy.auth import OAuthHandler
from weibopy.api import API
import time

try:
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

    f = open('/home/caq/smthcm/smthcm.config')
    cks = f.readline().strip().split('\t')
    tks = f.readline().strip().split('\t')
    f.close()
    # consumer_key, consumer_secret
    auth = OAuthHandler(cks[0], cks[1])
    # token, tokenSecret
    auth.setToken(tks[0], tks[1])
    api = API(auth)
    api.update_status(msg)
except:
    # raise
    pass
