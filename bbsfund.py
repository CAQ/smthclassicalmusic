# coding=utf-8

import sys, urllib
from weibopy.auth import OAuthHandler
from weibopy.api import API
from datetime import datetime
import time

try:
    wp = urllib.urlopen('http://www.newsmth.net/nForum/board/classicalmusic')
    content = wp.read(4000)
    content = content[0 : content.index('b-content corner')]
    contentutf8 = content.decode('gbk').encode('utf-8')
    ind1 = contentutf8.index('版面积分:')
    ind1 = contentutf8.index(':', ind1)
    ind2 = contentutf8.index('</span>', ind1)
    boardfund = contentutf8[ind1 + 1 : ind2]
    print str(datetime.now()) + '\t' + boardfund
    msg = '[' + time.strftime('%H:%M', time.localtime(time.time())) + '] 目前本版积分是' + boardfund + '，感谢版友们的支持，欢迎大家多多灌水，有条件的来捐献积分哦～'

    f = open('/home/caq/smthcm/smthcm.config')
    cks = f.readline().strip().split('\t')
    tks = f.readline().strip().split('\t')
    # consumer_key, consumer_secret
    auth = OAuthHandler(cks[0], cks[1])
    # token, tokenSecret
    auth.setToken(tks[0], tks[1])
    api = API(auth)
    api.update_status(msg)
except:
    raise
    # pass
