# -*- coding: utf-8 -*-

import urllib
import time, os
from datetime import datetime



TOTAL_SCORE = 30000
NOMINATE = {'chunzai':2}

SKIP_AUTHORS = ['CAQ9', 'deliver', 'SYSOP']



def print_dictionary(dictionary, keys_sorted, translate_keys=None, topk=-1):
    result = []
    if topk == 0:
        return result
    count = 0
    l = len(keys_sorted)
    lastvalue = None
    enough = False
    for key in keys_sorted:
        value = dictionary[key]
        if lastvalue != value and enough:
            break
        lastvalue = value
        count += 1
        print '\t', 
        if translate_keys is None:
            print ('未知' if key is None else key),
            if key is not None:
                result.append(key)
        else:
            if key in translate_keys:
                print translate_keys[key],
                result.append(translate_keys[key])
            else:
                print '未知',
                #result.append(None)
        print '\t', value, 
        if topk > 0:
            print ''
            if count >= topk:
                enough = True
        else:
            # print '\t', int(count * 10000.0 / l + 0.5) / 100.0, '%'
            print ''
    return result



def add_to_dict(dictionary, key, value=1):
    if key in dictionary:
        dictionary[key] += value
    else:
        dictionary[key] = value




def crawl(filename):
    f = open(filename, 'w')
    f.write('# postid, gid, author, flag, posttime, title, size, imported, is_tex\n')

    postinfos = []

    # Start at the latest page
    page_str = ''

    while True:

        # Crawl and parse the page
        print 'Crawling',
        conn = urllib.urlopen('http://www.newsmth.net/bbsdoc.php?board=ClassicalMusic&ftype=0' + page_str)
        content_gb2312 = conn.read()
        content_utf8 = content_gb2312.decode('gb2312', 'ignore').encode('utf-8')

        # var c = new docWriter('ClassicalMusic',24,21750,0,0,726,21779,'/groups/rec.faq/ClassicalMusic',1,1);
        ind0 = content_utf8.find('new docWriter(')
        boardinfo = content_utf8[content_utf8.find('(', ind0) + 1 : content_utf8.find(')', ind0)].strip()
        # 'ClassicalMusic',24,21750,0,0,726,21779,'/groups/rec.faq/ClassicalMusic',1,1
        (boardname, num1, current_page_start_num, num2, num3, current_page, therest) = boardinfo.split(',', 6)
        current_page = int(current_page)
        print 'page', current_page,

        # c.o(78035,78035,'CAQ9','d ',1316404312,'新浪微博 @水木古典音乐 欢迎关注 ',168,0,0);
        ind1 = content_utf8.find('c.o(')
        ind2 = content_utf8.rfind('c.t();')
        posts = content_utf8[ind1 : ind2].strip().split('c.o')
        page_mintime = -1
        page_maxtime = -1
        stored_count = 0
        for post in posts:
            # (78035,78035,'CAQ9','d ',1316404312,'新浪微博 @水木古典音乐 欢迎关注 ',168,0,0);
            if not post.startswith('('):
                continue
            t = post.strip()
            t = t[1 : len(t) - 2]
            # 78035,78035,'CAQ9','d ',1316404312,'新浪微博 @水木古典音乐 欢迎关注 ',168,0,0
            (postid, gid, author, flag, posttime, therest) = t.split(',', 5)
            (title, size, imported, is_tex) = therest.rsplit(',', 3)
            # Note we do it in 2 steps because title may contain commas

            # Refine the values
            postid = int(postid)
            gid = int(gid)
            author = author[1 : -1]
            flag = flag[1 : -1]
            posttime = datetime.fromtimestamp(int(posttime))
            title = title[1 : -1]
            size = int(size)
            imported = not (imported == '0')
            is_tex = not (is_tex == '0')

            if flag.find('d') >= 0:
                # Sticky bottom
                continue

            if page_mintime == -1 or posttime < page_mintime:
                page_mintime = posttime
            if page_maxtime == -1 or posttime > page_maxtime:
                page_maxtime = posttime

            if posttime >= startdate and posttime < enddate:
                fields = [postid, gid, author, flag, posttime, title, size, imported, is_tex]
                postinfos.append(fields)
                line = '\t'.join([x if type(x) == 'unicode' else str(x) for x in fields])
                f.write(line + '\n')
                stored_count += 1

        print stored_count, 'posts.'

        if page_mintime < startdate:
            # Stop crawling
            break

        page_str = '&page=' + str(current_page - 1)
        f.flush()
        time.sleep(1)


    # Now all posts have been crawled
    f.close()

    return postinfos



# MAIN

# Determine the time range of the posts
now = datetime.now()
#startdate = datetime(now.year + (now.month - 3) / 12, (now.month - 3) % 12 + 1, 1, 0, 0, 0, 0)
#enddate = datetime(now.year + (now.month - 2) / 12, (now.month - 2) % 12 + 1, 1, 0, 0, 0, 0)
startdate = datetime(2013, 1, 1, 0, 0, 0, 0)
enddate = datetime(2013, 7, 1, 0, 0, 0, 0)

filename = 'posts/' + startdate.strftime('%Y%m') + '-' + enddate.strftime('%Y%m') + '.txt'

# Read the posts information from file or crawling
postinfos = []
if not os.path.exists(filename):
    postinfos = crawl(filename)
else:
    f = open(filename)
    for line in f:
        if line.find('#') == 0:
            continue
        fields = line.strip().split('\t')
        postinfos.append(fields)
    f.close()


# Analysis begins

print filename
print '********************'
print '原始数据如下：'
print
print '该时期内帖子总数：', len(postinfos)

numposts = {} # author - num of posts
originals = {} # author - num of original posts
gid_author = {} # gid - author
markedposts = {} # author - num of marked posts
longposts = {} # author - num of long posts

LONG_THRESHOLD = 100

for postinfo in postinfos:
    # [postid, gid, author, flag, posttime, title, size, imported, is_tex]
    (postid, gid, author, flag, posttime, title, size, imported, is_tex) = tuple(postinfo)
    if author not in SKIP_AUTHORS:
        add_to_dict(numposts, author)
    if postid == gid:
        gid_author[gid] = author
        if author not in SKIP_AUTHORS:
            add_to_dict(originals, author)
    if flag.find('m') >= 0:
        if author not in SKIP_AUTHORS:
            add_to_dict(markedposts, author)
    if int(size) > LONG_THRESHOLD:
        if author not in SKIP_AUTHORS:
            add_to_dict(longposts, author)

original_replies = {} # author - num of posts replied by others
for postinfo in postinfos:
    (postid, gid, author, flag, posttime, title, size, imported, is_tex) = tuple(postinfo)
    if postid == gid:
        continue
    original_author = gid_author[gid] if gid in gid_author else None
    if author == original_author or original_author in SKIP_AUTHORS:
        continue
    add_to_dict(original_replies, original_author)


reward_post = []

numposts_sorted = sorted(numposts, key=lambda x: -numposts[x])
print '发文数',
print '（发文作者人数', len(numposts), '）'
rewarded = print_dictionary(numposts, numposts_sorted, topk=10)
for r in rewarded:
    reward_post.append(r)

originals_sorted = sorted(originals, key=lambda x: (-originals[x], x))
print '原创数',
print '（原创作者人数', len(originals), '）'
rewarded = print_dictionary(originals, originals_sorted, topk=20)
for r in rewarded:
    reward_post.append(r)

original_replies_sorted = sorted(original_replies, key=lambda x: -original_replies[x])
print '发表原创引来的其他人回复数',
print '（该部分作者人数', len(original_replies), '）'
rewarded = print_dictionary(original_replies, original_replies_sorted, topk=10)
for r in rewarded:
    reward_post.append(r)

markedposts_sorted = sorted(markedposts, key=lambda x: -markedposts[x])
print '被m的帖子数',
print '（作者人数', len(markedposts), '）'
rewarded = print_dictionary(markedposts, markedposts_sorted)
for r in rewarded:
    reward_post.append(r)

longposts_sorted = sorted(longposts, key=lambda x: -longposts[x])
print '长文数（长度 >', LONG_THRESHOLD, '）',
print '（该部分作者人数', len(longposts), '）'
rewarded = print_dictionary(longposts, longposts_sorted, topk=10)
for r in rewarded:
    reward_post.append(r)

print '********************'
print '本次奖励积分数：', TOTAL_SCORE
print '发帖奖励总人次：', len(reward_post)

nominate_sum = sum(NOMINATE[x] for x in NOMINATE)
print '提名指标：', nominate_sum

zhuban = []
f = open('zhuban.txt')
for line in f:
    zhuban.append(line.strip())
f.close()
print '驻版指标：', 1, '，由', len(zhuban), '人共享'

unit_score = TOTAL_SCORE / (len(reward_post) + nominate_sum + 1)
print
print '每个指标', unit_score, '分，',

reward_result = {}
for r in reward_post:
    add_to_dict(reward_result, r)
for r in NOMINATE:
    add_to_dict(reward_result, r, value=NOMINATE[r])
for r in zhuban:
    add_to_dict(reward_result, r, value=(1.0 / len(zhuban)))
print '奖励共', len(reward_result), '人，名单如下：'

reward_result_sorted = sorted(reward_result, key=lambda x:x.lower())
total1 = 0
total2 = 0
print 'ID\t指标数\t积分'
for r in reward_result_sorted:
    value1 = int(reward_result[r] * 100.0 + 0.5) / 100.0
    value2 = int(reward_result[r] * unit_score)
    print r, '\t', value1, '\t', value2
    total1 += value1
    total2 += value2
print '总计\t', total1, '\t', total2


print '********************'
print '提名ID\t加权系数'
for r in NOMINATE:
    print r, '\t', NOMINATE[r]

print
print '当前驻版：',
for r in zhuban:
    print r,
