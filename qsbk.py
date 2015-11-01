#!/usr/bin/env python
# encoding: utf-8

import urllib2, urllib, os, re, socket, requests

socket.setdefaulttimeout(25)

"""
@version: 1.0
@author: hiphp
@license: Apache Licence 
@contact: hi_php@163.com
@site: wuwenfu.cn
@software: PyCharm Community Edition
@file: qsbk.py
@time: 2015/10/31 21:34
"""


# 读取网页，
def get_html(url):
    html = ''
    r = requests.get(url)
    html = r.text
    return html
#获取段子.传递一个列表地址与 当前的页码
def save_duanzi(page,url):
    html = get_html(url)
    #存放段子的序列
    dzs =[]
    p = re.compile('<div class="article block.*?">.*?<div class="content">(.*?)<!--.*?</div>.*?</div>',re.S)
    rs = re.findall(p,html)
    if(rs and len(rs) > 0):
        for item in rs:
            # print item
             #再次过滤，去掉非中文字符
            item = re.findall(u"[\u4e00-\u9fa5]+",item)
            # print item
            dzs.append(''.join(item))
            # print("----------------------------------------------")
    else:
        print(u"匹配内容为空")
    #写入记事本.追加的模式
    f = open(u"c:\\糗事百科%s.txt" % page,"w+")
    i =0
    for item in dzs:
        i +=1
        f.write("\r\n-------------------段子%s---------------------------------\n" % i)
        # print item
        temp = item.encode('utf8', 'ignore')
        # print temp
        f.write(temp)
        f.write("\r\n-------------------段子%s---------------------------------\n" % i)
    f.flush()
    f.close()

class Main():
    def __init__(self):
        pass


if __name__ == '__main__':
    #获取所有的段子列表。
    links = ["http://www.qiushibaike.com/textnew/page/%s?s=4820993" % i for i in xrange(1,35) ]
    page =1
    for link in links:
        print(u"在处理第%s页:%s" %(page,link))
        save_duanzi(page,link)
        page +=1
