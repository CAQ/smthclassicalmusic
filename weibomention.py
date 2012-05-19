# coding=utf-8

import urllib, urllib2
from weibopy.auth import OAuthHandler
from weibopy.api import API
import cookielib
import time

def retweetit(msg):
    global api, myfriends, retweeted

    id = str(msg['id'])
    userid = msg['user'].__getattribute__('id')
    if userid in myfriends and not id in retweeted:
        #print 'repost', id, msg['text']
        #api.repost(id, '') ## do not add anything when retweet
        #fw = open('/home/caq/smthcm/retweeted.txt', 'a')
        #fw.write(str(id) + '\n')
        #fw.close()
        time.sleep(5)
    else:
        print userid, id

try:
    f = open('/home/caq/smthcm/smthcm.config')
    cks = f.readline().strip().split('\t')
    tks = f.readline().strip().split('\t')
    usrpwd = f.readline().strip().split('\t')
    f.close()
    auth = OAuthHandler(cks[0], cks[1])
    auth.setToken(tks[0], tks[1])
    api = API(auth)

    myfriends = api.friends_ids(count=5000).__dict__['ids']

    f = open('/home/caq/smthcm/posted.txt') ## for bbs posts
    posted = f.read().splitlines()
    f.close()
    f = open('/home/caq/smthcm/retweeted.txt') ## for weibo retweet
    retweeted = f.read().splitlines()
    f.close()

    combinedweibos = {} ## key: retweet id, value: messages to post

    for mention in api.mentions(count=100):
        mentiondict = mention.__dict__
        histext = mentiondict['text'].strip().encode('utf-8')
        if not str(mentiondict['id']) in posted: ## hasn't been posted before
            if mentiondict.has_key('retweeted_status'):
                id = mentiondict['retweeted_status'].__getattribute__('id')
            else:
                id = mentiondict['id']
            id = str(id)
            if combinedweibos.has_key(id):
                value = combinedweibos[id]
                value.append(mentiondict)
            else:
                value = [mentiondict]
            combinedweibos[id] = value
            fw = open('/home/caq/smthcm/posted.txt', 'a')
            fw.write(str(mentiondict['id']) + '\n')
            fw.close()

        if '@水木古典音乐' in histext: ## if he mentioned me in his main content, retweet it
            retweetit(mentiondict)
        else: ## he didn't mention me, then there must be a retweeted status
            if not mentiondict.has_key('retweeted_status'):
                continue
            rtdict = mentiondict['retweeted_status'].__dict__
            retweettext = rtdict['text'].strip().encode('utf-8')
            retweetuserid = rtdict['user'].__dict__['id']
            if retweetuserid == 2408847334: ## he retweeted my post
                if len(histext) > len('转发微博。'): ## this retweet is valuable, retweet his post
                    retweetit(mentiondict)
            else: ## the original tweet wasn't by me, it must have mentioned me. retweet his post
                retweetit(mentiondict)

    bbspost = '欢迎关注新浪微博 @水木古典音乐 http://www.weibo.com/smthclassicalmusic\n\n'
    for id in combinedweibos:
        comments = ''
        pureretweets = ''
        rtdict = None
        for msg in combinedweibos[id]:
            if msg.has_key('retweeted_status'):
                rtdict = msg['retweeted_status'].__dict__
            if str(msg['id']) == str(id):
                continue
            msgtext = msg['text'].encode('utf-8').strip()
            if msgtext == '转发微博。' or msgtext == '转发微博':
                pureretweets = '@' + msg['user'].__getattribute__('screen_name').encode('utf-8') + ' '
            else:
                comments += '@' + msg['user'].__getattribute__('screen_name').encode('utf-8') + ' 在' + str(msg['created_at']) + '说：' + msgtext + '\n'

        if rtdict is not None:
            bbspost += '@' + rtdict['user'].__getattribute__('screen_name').encode('utf-8') + ' 在' + str(rtdict['created_at']) + '发表：' + rtdict['text'].encode('utf-8').strip() + '\n'
        if len(comments) > 0 and len(pureretweets) > 0:
            bbspost += comments + '还被' + pureretweets + '转发了。\n'
        elif len(comments) == 0 and len(pureretweets) > 0:
            bbspost += '被' + pureretweets + '转发了。\n'
        elif len(comments) > 0 and len(pureretweets) == 0:
            bbspost += comments
        bbspost += '\n'

    if len(combinedweibos) > 0:
        #print bbspost
        post_data = urllib.urlencode({'id': usrpwd[0], 'passwd': usrpwd[1]})
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        opener.addheaders = [('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1')]
        urllib2.install_opener(opener)
        req = urllib2.Request('http://m.newsmth.net/user/login', post_data)
        conn = urllib2.urlopen(req)
        time.sleep(3)
        post_data = urllib.urlencode({'subject': '微博互动', 'content': bbspost})
        req = urllib2.Request('http://m.newsmth.net/article/ClassicalMusic/post', post_data)
        urllib2.urlopen(req)
        time.sleep(3)
        req = urllib2.Request('http://m.newsmth.net/user/logout', post_data)
        conn = urllib2.urlopen(req)

except:
    raise
    # pass
