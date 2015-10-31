#!/usr/bin/env python
# encoding: utf-8
import urllib2,urllib,os,re,socket,requests
socket.setdefaulttimeout(25)

import time

"""
@version: 1.0
@author: hiphp
@license: Apache Licence 
@contact: hi_php@163.com
@site: wuwenfu.cn
@software: PyCharm Community Edition
@file: Naruto.py
@主要是采集起点的小说








"""


def func():
    pass

#起点类。下载起点小说。
#这里先通过下载 第 42页的起点小说列表，来演示。通过这一个，就可以下载所有的小说。

class Qidian():
    #构造函数
    def __init__(self,urls):
        self.urls = urls
        # self.url =  'http://all.qidian.com/Book/BookStore.aspx?ChannelId=-1&SubCategoryId=-1&Tag=all&Size=-1&Action=5&OrderId=6&P=all&PageIndex=42&update=-1&Vip=-1&Boutique=-1&SignStatus=-1' #漫画列表 #地址
        self.books = []
        #books 表示所有小说，是一个序列[].book是它的元素。
        #book 表示每一本小说，它是个字典：包含 书名、title 书的编号、bookid   书的起点链接link  章节的入口 chapterlink  章节列表 chapterlist
        #chapterlist 是一个序列。chapter 是它的元素。
        #chapter  表示每一章节。是字典：包含章节名称 章节的链接 章节的内容。 就是一篇文章。



    #读取网页，
    def get_html(self,url):
        html = ''
        try:
            html = urllib2.urlopen(url).read()
        except Exception,e:
            print(u'打开网页%s错误:%s'% (url,e.message))
        return html

    #获取网页的第二个方法。
    def get_html2(self,url):
        html = ''
        r = requests.get(url)
        html = r.text
        return html
    #获得所有书籍
    def get_allbook(self):
        for url in self.urls:
            self.get_books(url)

    #获取某一个列表的所有书籍。
    def get_books(self,url):
        print(u"处理列表:%s"% url)

        html = self.get_html2(url)
        if(html):
            p1 = re.compile('<a.*?href="http://www.qidian.com/Book/(\d+).aspx" target="_blank">(.*?)</a>',re.S)
            rs = re.findall(p1,html)
            if(rs and len(rs)>0):
                for item in rs:
                    # print(item)
                    # print item[0]
                    # print(item[1])
                    # title = item[1].decode('utf-8','ignore')
                    title  =item[1]
                    p=re.compile('\s+');
                    title = re.sub(p,'',title)

                    #再次过滤，去掉非中文字符
                    rs1 = re.findall(u"[\u4e00-\u9fa5]+",title)
                    title =rs1[0]


                    booid = item[0]
                    link = 'http://www.qidian.com/Book/%s.aspx'% (item[0])
                    self.books.append({'title':title,'bookid':booid,'link':link,'chapterlist':[]})
            else:
                print(u'没有发现书籍:页面未找到')
        else:
            print(u'没有发现书籍:页面为空')


    #获取书籍的章节。获取指定书籍的章节。参数为书籍的字典。
    #获取每本小说的章节入口链接。通过书的链接，得到章节的链接入口


    def get_chapterlink(self,book):
        html = self.get_html2(book['link'])
        if(html):
            p1 = re.compile('<a.*?href="http://read.qidian.com/BookReader(.*?)".*?>(.*?)</a>',re.S)
            rs = re.findall(p1,html)
            if(rs and len(rs)>0):
                for item in rs:
                    if(item[1] == u"点击阅读"):
                        # print(item[0])
                        book['chapterlink'] = 'http://read.qidian.com/BookReader%s' % item[0] #书的章节列表
            else:
                print(u'没有发现章节入口链接:页面未找到')
        else:
            print(u'没有发现章节入口链接:页面为空')
    #通过章节入口，获取所有的章节列表
    def get_chapterlist(self,book):
        html = self.get_html2(book['chapterlink'])
        if(html):
            p1 = re.compile('<li.*?chapter.*?><a.*?href="(.*?)".*?><span.*?>(.*?)</span></a></li>',re.S)
            rs = re.findall(p1,html)
            # print rs
            if(rs and len(rs)>0):
                for item in rs:
                    # print item[0]
                    # print item[1]
                    title = item[1]
                    #这里去掉一次空白字符串
                    p=re.compile('\s+');
                    title = re.sub(p,'',title)
                    #再次过滤，去掉非中文字符
                    rs1 = re.findall(u"[\u4e00-\u9fa5]+",title)
                    title =rs1[0]

                    book['chapterlist'].append({'title':title,'link':item[0]})
            else:
                print(u'没有发现章节列表:页面未找到')
        else:
            print(u'没有发现章节列表:页面为空')
    #获取小说的正文
    #小说内容没有直接在html中，而是在一个txt文件。
    #
    def get_chaptercontent(self,book, chapter):
        chapter['link']="http://read.qidian.com/BookReader/3gYCGvlOH9E1,9t3aUOmIYGo1.aspx"
        html = self.get_html2(chapter['link'])
        # print(html)
        if (html):
            # 匹配正文
            p1 = re.compile('<script src=\'http://files.qidian.com/(.*?).txt\'  charset=\'GB2312\'></script>', re.S)
            rs = re.findall(p1, html)
            if (rs and len(rs) > 0):
                print(rs)
                #这里只是获取了文章的链接，
                txturl = "http://files.qidian.com/%s.txt" % rs[0]

                print(txturl)
                #获取txt文件内容.有可能是加密的。无法直接获取字符串，因为是txt文件，编码可能是aci
                # txt = self.get_html2(txturl);
                #定义一个目录。c:\\起点小说
                #存放规则，是按照每一本小说来存放。每一章保存为一个txt文本。
                #最终的结果是c:\\起点小说\\xx小说\\xx章节.txt
                #需要创建每一本书的目录
                path = u"c:\\起点小说\\%s" % book['title']
                #如果不存在目录，则创建。
                if not(os.path.exists(path)):
                    os.mkdir(path)


                filename = u"c:\\起点小说\\%s\\%s.txt" % (book['title'],chapter['title'])
                print(u"%s"% filename)

                #如果该文件存在，则不用再次下载。
                if(os.path.exists(filename)):
                    print(u"该章节已经下载过了")

                urllib.urlretrieve(txturl,filename);
                print(u'保存文件ok')
                # print(txt)
            else:
                print(u'匹配正文时为空')
        else:
            print(u'获取小说正文网页为空')

if __name__ == '__main__':

    s1 = u"时间：2015年10月31日"
    s2 = u"作者：吴文付 hi_php@163.com"
    s3 = u"描叙:下载起点中文的全本小说.默认的下载目录为c:\\起点小说。"
    screen_width = 200

    text_width = len(s1+s2+s3)
    box_width = text_width+6

    left_margin = (screen_width-box_width)//2

    print
    print ' '+'+'+'-'*(box_width-2)+'+'
    print ' '+'| '
    print ' '+'| '+s1
    print ' '+'| '+s2
    print ' '+'| '+s3
    print ' '+'| '
    print ' '+'+'+'-'*(box_width-2)+'+'
    print

    print(u'请选择需要哪几个列表的小说，最大为43(如输入1则下载第一页，输入1,5这表示下载第一页与第五页。如果输入1:5 这表示下载第1页到第5页):')
    id = raw_input()

    ids = [] #需要下载的书籍序列。
    #判断是否包含,或者:
    if(id.find(',') >=0):
        #表示有选择性下载。
        temp = id.split(',')
        #转为数字。
        for id in temp:
            ids.append(int(id))

    if(id.find(':')>=0):
        #表示是区间下载。
        temp = id.split(':')
        ids = range(int(temp[0]),int(temp[1])+1)
    #如果上面一个都不是。则是指定下载某一本。

    if (len(ids) ==0):
        ids.append(int(id))

    #进行一次排序。
    ids.sort()





    #我们需要下载所有的全本小说。从第一页从第43页
    #http://all.qidian.com/Book/BookStore.php?ChannelId=-1&SubCategoryId=-1&Tag=all&Size=-1&Action=5&OrderId=6&P=all&PageIndex=1&update=-1&Vip=-1&Boutique=-1&SignStatus=-1
    #http://all.qidian.com/Book/BookStore.aspx?ChannelId=-1&SubCategoryId=-1&Tag=all&Size=-1&Action=5&OrderId=6&P=all&PageIndex=2&update=-1&Vip=-1&Boutique=-1&SignStatus=-1

    #对比以后发现，就 PageIndex =1 这个参数不同

    #产生所有的列表的页面。
    # links = ["http://all.qidian.com/Book/BookStore.aspx?ChannelId=-1&SubCategoryId=-1&Tag=all&Size=-1&Action=5&OrderId=6&P=all&PageIndex=%s&update=-1&Vip=-1&Boutique=-1&SignStatus=-1" % i for i in xrange(1,5) ]
    links = []
    for id in ids:
        links.append("http://all.qidian.com/Book/BookStore.aspx?ChannelId=-1&SubCategoryId=-1&Tag=all&Size=-1&Action=5&OrderId=6&P=all&PageIndex=%s&update=-1&Vip=-1&Boutique=-1&SignStatus=-1" % id)

    #创建对象
    qidian = Qidian(links)

    #获取所有书籍
    qidian.get_allbook()

    for book in qidian.books:

        print(u'正在处理小说:%s'%book['title'])
        print(book['link'])

        #获取章节入口链接
        qidian.get_chapterlink(book)

        print(book['chapterlink'])
        #开始获取所有章节
        qidian.get_chapterlist(book)
        i = 0
        for chapter in book['chapterlist']:
            #如果不包含xx章。则跳过处理。
            i += 1
            if(i ==1):
                continue
            print('title:%s '% chapter['title'])
            print('link:%s' % chapter['link'])

            #开始对每一个章节进行处理。
            qidian.get_chaptercontent(book,chapter)
            #成功保存了文件。
            # exit()
        # exit()


    #打印所有书籍
    # i = 0
    # for book in qidian.books:
    #     i +=1
    #     print u"第%s本小说:%s" % (i,book['title'])





    exit()


    qidian = Qidian()
    qidian.get_books()
    # print(qidian.books)
    # exit()
    #已经获得书籍。
    for book in qidian.books:

        print(u'正在处理小说:%s'%book['title'])
        print(book['link'])

        #获取章节入口链接
        qidian.get_chapterlink(book)

        print(book['chapterlink'])
        #开始获取所有章节
        qidian.get_chapterlist(book)
        i = 0
        for chapter in book['chapterlist']:
            #如果不包含xx章。则跳过处理。
            i += 1
            if(i ==1):
                continue
            print('title:%s '% chapter['title'])
            print('link:%s' % chapter['link'])

            #开始对每一个章节进行处理。
            qidian.get_chaptercontent(book,chapter)
            #成功保存了文件。
            # exit()
        # exit()
