# -*- coding: utf-8 -*-
'''
fetch and extract `today in classical music' from http://cdexchang.blogspot.com
'''
from bs4 import BeautifulSoup, element
import datetime, urllib, re, os

# deprecated
def get_everyday_links_racampbell():
    count = 0
    fw = open('everydaylinks.txt', 'w')
    # 12 months
    for monthid in range(10, 22):
        url = 'http://racampbell.tripod.com/almanac/id' + str(monthid) + '.html'
        soup = BeautifulSoup(urllib.urlopen(url).read())
        for tr in soup.find_all('tr', valign='middle'):
            links = tr.find_all('a')
            if links is None:
                continue
            # days in a month
            for link in links:
                fw.write(link.get('href') + '\n')
                count += 1
    fw.close()
    return count

def get_everyday_links():
    begindate = datetime.date(2012, 1, 1)
    enddate = datetime.date(2012, 12, 31)
    oneday = datetime.timedelta(days=1)
    dt = begindate
    fw = open('everydaylinks.txt', 'w')
    count = 0
    while dt <= enddate:
        url = 'http://www.musiclassical.net/' + dt.strftime('%b/%d').upper() + '.html'
        #datestr = dt.strftime('%m%d')
        # get the html page
        soup = BeautifulSoup(urllib.urlopen(url).read())
        for link in soup.find_all('a'):
            href = link.get('href')
            if href.find('http://cdexchang.blogspot.com/') != 0:
                continue
            fw.write(link.get('href') + '\n')
            count += 1
        dt += oneday
    fw.close()
    return count

def get_eachday(url):
    # get the html page
    soup = BeautifulSoup(urllib.urlopen(url, proxies={'http':'http://localhost:8087'}).read())
    block = soup.find('div', class_='post hentry')
    if block is None:
        return
    title = block.find('h3').get_text()
    content = block.find('div', class_='post-body entry-content')
    filename = 'data/' + title.strip().replace(' ', '-') + '.txt'
    print filename
    fw = open(filename, 'w')
    fw.write(content.prettify().encode('utf-8'))
    fw.close()

def get_everyday():
    count = 0
    f = open('everydaylinks.txt')
    for line in f:
        if count > 20:
            get_eachday(line.strip())
        count += 1
    f.close()

months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
pattern = '(' + '|'.join(months) + ')-[0-9]+'
def rename():
    global pattern
    base = './data/'
    for filename in os.listdir(base):
        if filename.find('.txt') < 0:
            print 'Error:', filename
            continue
        match = re.search(pattern, filename.lower())
        if match:
            newname = match.group(0)
            if os.path.exists(base + newname):
                print 'Exists:', newname
            else:
                os.rename(base + filename, base + newname + '.txt')
        else:
            print 'Error:', filename

def extract_items():
    global months
    fw = open('events.txt', 'w')

    base = './data/'
    for filename in os.listdir(base):
        monthname, d = filename[ : -4].split('-')
        m = str(months.index(monthname) + 1)
        if len(m) < 2:
            m = '0' + m
        if len(d) < 2:
            d = '0' + d
        datestr = m + d
        f = open(base + filename)
        soup = BeautifulSoup(f)
        for child in soup.find('div').children:
            if type(child) is not element.Tag:
                continue
            if child.name == 'li':
                text = ''
                imgs = []
                for son in child.children:
                    if type(son) is element.NavigableString:
                        text += son.encode('utf-8').strip() + ' '
                    elif type(son) is element.Tag:
                        if son.name == 'a':
                            text += son.get_text().encode('utf-8').strip() + ' '
                            if son.find('img') is not None:
                                imgs.append(son.find('img').get('src'))
                        elif son.name == 'img':
                            if son.get('height') != '1':
                                imgs.append(son.get('src'))
                    else:
                        print filename, son
                text = re.sub('\s+', ' ', text).strip()
                if len(text) <= 0:
                    continue
                year = '9999'
                match = re.search('^[0-9]+ ', text)
                if match:
                    year = match.group(0).strip()
                match = re.search(' (Birth|Death|FP) of ', text)
                if match:
                    eventtype = match.group(1)
                else:
                    eventtype = 'Other'
                fw.write('\t'.join([datestr, year, eventtype, text]) + '\t'.join(imgs) + '\n')
        f.close()
    fw.close()

# print get_everyday_links()
# get_everyday()
# rename()
extract_items()
