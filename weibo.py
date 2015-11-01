#!/usr/bin/env python
# encoding: utf-8


"""
@version: 1.0
@author: hiphp
@license: Apache Licence 
@contact: hi_php@163.com
@site: wuwenfu.cn
@software: PyCharm Community Edition
@file: weibo.py.py
@time: 2015/11/1 15:26

糗事百科： http://weibo.com/206264040





"""
import urllib2,urllib,os,re,socket,requests,json
socket.setdefaulttimeout(25)


#获取网页的第二个方法。
def get_html2(url):
    html = ''
    r = requests.get(url)
    html = r.text
    return html
#需要添加headers



def get_html(url):
    html = ''
    request = urllib2.Request(url)
    #这里依次添加数据。
    request.add_header('Host', 'weibo.com')
    request.add_header("User_Agent","Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0")
    request.add_header("Accept","text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
    request.add_header("Accept-Language","zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3")
    request.add_header("Referer","http://s.weibo.com/weibo/%25E7%25B3%2597%25E4%25BA%258B%25E7%2599%25BE%25E7%25A7%2591?topnav=1&wvr=6&b=1")
    request.add_header("Cookie","UOR=news.china.com.cn,widget.weibo.com,news.china.com.cn; YF-Page-G0=dd6e6fbf5c2a69c431a9b269961f330f; login_sid_t=417f7a9fff5a86182c894f6c5660e570; YF-Ugrow-G0=56862bac2f6bf97368b95873bc687eef; _s_tentry=passport.weibo.com; Apache=4480505128750.847.1446363749634; SINAGLOBAL=4480505128750.847.1446363749634; ULV=1446363749690:1:1:1:4480505128750.847.1446363749634:; crossidccode=CODE-gz-1zSNil-3mlOiL-0PSLXSGF92LnYID213d7d; SUS=SID-1640433933-1446363802-GZ-i1uyt-83d17a204dc1478d310132b812d687fc; SUE=es%3D4759ce32515f7d6641a6559bfc30a178%26ev%3Dv1%26es2%3D6b94dc1492c788dec9ed2da963e16b3a%26rs0%3DI94i%252FnEwSIlyvkxiIjhVTpNk7eifr1x7PNufpGFRzPfUp0Nc5EtwVTyPip%252FLcOkSrz53gb67cwLC%252Fjbu3F16YGY9o49S%252BpRoqJogC32DO3iTDbDm%252F%252FZRJF2XltiCsY81qKeR6fP2QAX2Xojb5Zb8DvDzRKpuY9jB50Gt5NcFgTo%253D%26rv%3D0; SUP=cv%3D1%26bt%3D1446363802%26et%3D1446450202%26d%3Dc909%26i%3D87fc%26us%3D1%26vf%3D0%26vt%3D0%26ac%3D2%26st%3D0%26uid%3D1640433933%26name%3Dsudawuwenfu%2540sina.com%26nick%3D%25E8%25B1%2586%25E8%25B1%2586%25E5%2590%2583%25E8%25B1%2586%26fmp%3D%26lcp%3D2014-05-15%252012%253A55%253A23; SUB=_2A257MbLKDeTxGedI71IV8y3FyD-IHXVYRqMCrDV8PUNbu9BeLXD2kW-RzrUvIG-RZdQolUsyvG60y06RHg..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5aGifP59Hn68kwULh_Z5yS5JpX5Kzt; SUHB=0FQqorvI5qnivV; ALF=1477899801; SSOLoginState=1446363801; wvr=6; YF-V5-G0=3717816620d23c89a2402129ebf80935")
    request.add_header("Connection","keep-alive")
    request.add_header("Cache-Control","max-age=0")


    response = urllib2.urlopen(request)


    html = response.read()

    # html = unicode(html,'GBK').encode('UTF-8')

    # try:
    #     html = urllib2.urlopen(url).read()
    # except Exception,e:
    #     print(u'打开网页%s错误:%s'% (url,e.message))
    return html

#存储为文本
#传递的是解析好的序列。
def save_duanzi(page,weibo):
    #写入记事本.追加的模式
    f = open(u"c:\\微博糗事大百科%s.txt" % page,"w+")
    i =0
    for item in weibo:
        i +=1
        f.write("\r\n-------------------微博%s---------------------------------\n" % i)
        temp = item.encode('utf8', 'ignore')
        # print temp
        f.write(temp)
        f.write("\r\n-------------------微博%s---------------------------------\n" % i)
    f.flush()
    f.close()

def func():
    pass


class Main():
    def __init__(self):
        pass


if __name__ == '__main__':


    #共有分页265页，这里只获取5页微博内容。
    links = ["http://weibo.com/206264040?is_search=0&visible=0&is_ori=1&is_tag=0&profile_ftype=1&page=%d#feedtop" % i for i in xrange(4,10)]
    page = 0
    for link in links:
        page +=1
        print(u"正在处理糗事大百科的第%s页:%s" %(page,link))

        #直接处理获得数据。分3次进行。

        #第一次:
        html = get_html(link)

        #第一次获取的数据，存储为文件，再读取一次。
        # f = open("c:\\weibo%d.html"% page,"w")
        # f.write(html)
        # f.close()
        #
        # exit()

        p = re.compile('<div.*?WB_text.*?>(.*?)/div>',re.S)
        rs = re.findall(p,html)
        weibos = []
        if(rs  and  len(rs)>0 ):
            for item in rs:
                #只提取中文，其他的字符过滤
                item = item.decode("utf-8")
                rs1 = re.findall(u"[\u4e00-\u9fa5]+",item)
                # print(''.join(rs1))
                #存储为txt文件。
                weibos.append(''.join(rs1))
        else:
            print(u"匹配内容为空1")
        # save_duanzi(1,weibos)

        #第二次:
        link_second = "http://weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain=100505&is_search=0&visible=0&is_tag=0&profile_ftype=1&page=%d&pre_page=%d&max_id=&end_id=3900474299809609&pagebar=0&filtered_min_id=&pl_name=Pl_Official_MyProfileFeed__21&id=1005051720084970&script_uri=/206264040&feed_type=0&domain_op=100505&__rnd=1446369043509" % (page,page-1)

        jsonstr = get_html(link_second)
        #这里要对json数据进行处理。
        d = json.loads(jsonstr)
        data = d['data']
        p = re.compile('<div.*?WB_text.*?>(.*?)/div>',re.S)
        rs = re.findall(p,data)

        if(rs  and  len(rs)>0 ):
            for item in rs:
                #需要替换所有空白字符串，
                p=re.compile('\s+');
                item = re.sub(p,'',item)
                rs1 = re.findall(u"[\u4e00-\u9fa5]+",item)
                weibos.append(''.join(rs1))
        else:
            print(u"匹配内容为空2")

        #第三次
        link_third = "http://weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain=100505&is_search=0&visible=0&is_tag=0&profile_ftype=1&page=%s&pre_page=%s&max_id=&end_id=3900474299809609&pagebar=1&filtered_min_id=&pl_name=Pl_Official_MyProfileFeed__21&id=1005051720084970&script_uri=/206264040&feed_type=0&domain_op=100505&__rnd=1446369043509" % (page,page-1)

        jsonstr = get_html(link_third)
        #这里要对json数据进行处理。
        d = json.loads(jsonstr)
        data = d['data']
        p = re.compile('<div.*?WB_text.*?>(.*?)/div>',re.S)
        rs = re.findall(p,data)

        if(rs  and  len(rs)>0 ):
            for item in rs:
                #需要替换所有空白字符串，
                p=re.compile('\s+');
                item = re.sub(p,'',item)
                rs1 = re.findall(u"[\u4e00-\u9fa5]+",item)
                weibos.append(''.join(rs1))
        else:
            print(u"匹配内容为空3")







        #获得所有数据后，再存储。
        save_duanzi(page,weibos)









        #处理完第一页的就退出。
        # exit()





    exit()




    # url = "http://weibo.com/206264040"
    # url = "http://weibo.com/206264040?profile_ftype=1&is_ori=1#_0"
    # html = get_html2(url)
    # html = get_html(url)
    # html = html.decode("gbk","ignore")
    # print(html)
    #获取的数据写入文件
    # f = open("c:\\weibo.html","w")
    # f.write(html)
    # f.close()
    # exit()

    #依次爬去微博的数据，存储为文件，然后从文件中获取数据，再来解析匹配

    f = open("c:\\weibo.html","r")
    html = f.read()
    f.close()

    # print(html)

    # print(html.find("WB_text"))

    # exit()







    #匹配原创微博的正则内容。

    p = re.compile('<div.*?WB_text.*?>(.*?)/div>',re.S)
    rs = re.findall(p,html)
    weibos = []

    if(rs  and  len(rs)>0 ):
        for item in rs:
            #只提取中文，其他的字符过滤
            item = item.decode("utf-8")
            rs1 = re.findall(u"[\u4e00-\u9fa5]+",item)
            # print(''.join(rs1))
            #存储为txt文件。
            weibos.append(''.join(rs1))
    else:
        print(u"匹配内容为空")

    save_duanzi(1,weibos)


    #http://weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain=100505&pre_page=1&page=1&max_id=&end_id=3904365410160514&pagebar=1&filtered_min_id=&pl_name=Pl_Official_MyProfileFeed__21&id=1005051720084970&script_uri=/206264040&feed_type=0&domain_op=100505&__rnd=1446368582316













