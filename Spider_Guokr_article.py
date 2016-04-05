#果壳网科幻短篇小说爬虫
#思路
''''

    1、两层循环，外循环逐个访问不同页数，内循环逐个访问当前页面内不同文章
    2、内循环进入文章后，通过正则表达式，获取文章标题、作者、译者、文章主体
    3、内循环每获取一篇文章，就采用追加的方式写入指定txt文本中

'''''

__author__ = 'yff'

import requests
from io import StringIO
from pathlib import _Accessor
from bs4 import BeautifulSoup

import re
#id="articleTitle">(.*?)</h1>.*?<meta.*?content="(.*?)".*?>.*?<td class="field-body">(.*?)</td>.*?<td class="field-body">(.*?)</td>.*?<p>(.*?)<div class="line-block">
aurl= '/article/49513'
reArticleUrl = re.compile('class="title-detail">.*?<a.*?href="(.*?)"',re.S)
reArticleName = re.compile('id="articleTitle">(.*?)</h1>',re.S)
reArticleShort = re.compile('id="articleTitle">.*?content="(.*?)".*?>',re.S)
reArticleAuthor = re.compile('<td.*?class="field-body">(.*?)</td>',re.S)
reArticleCont = re.compile('class="document">.*?<p>(.*?)class="copyright">',re.S)
book_id = 0
def getPage():
    global book_id
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36'}
    #已知100页
    for i in range(1,100):
        #外部循环获取每一页的内容
        outside_url = 'http://m.guokr.com/search/article/?page='+str(i)+'&wd=%E5%B0%8F%E8%AF%B4'
        r = requests.get(outside_url,headers = headers)
        page_content = r.text
        #print(page_content)
        #获取这一页的文章数量
        aurl = re.findall(reArticleUrl,page_content)
        #print(aurl) 
        for j in aurl:
            try:
                inside_url = 'http://www.guokr.com' + j
                #print(inside_url)
                rr = requests.get(inside_url,headers = headers)
                rr = rr.text
                #print(rr)
                name= re.findall(reArticleName,rr)
                if(len(name)==0):
                    ss = "无名文"
                else:
                    ss = name[0]
                print(">>>>正在写入文章，目前第"+str(i)+"页，文章名:"+ss)
                #print(name)
                short = re.findall(reArticleShort,rr)                
                #print(short)
                author = re.findall(reArticleAuthor,rr)
                #print(author)
                content = re.findall(reArticleCont,rr)
                if(not(content)):
                    print(">>>>本次抓取文章失败，原因：空内容")
                    continue
                bs4_content = BeautifulSoup(content[0],"lxml")
                #print(bs4_content.get_text())
                #写入文件
                book_id =book_id + 1
                writeinFile(name,short,author,bs4_content.get_text(),book_id)
            except:
                continue
            
            
def writeinFile(n,s,a,c,b):
    if len(a)==0:
        a = "佚名"
    elif len(a) ==1:
        a = '作者：'+a[0]
    else:
        a = "作者：" + a[0] + "\n译者："+a[1]
        
    if(len(n)==0):
        n = "无名文"
    else:
        n = n[0]
        
    s = s[0]
    filename = 'No：'+str(b)+'：'+n+'.txt'
    #print(filename)
    try:
        with open(filename,'w',encoding='utf-8') as file:
            file.write(n)
            file.write('\n')
            file.write(s)
            file.write('\n')
            file.write(a)
            file.write('\n')
            file.write('==============正文=============\n')
            file.write(c)
    except IOError:
            print('File error:'+str(err))

    
        
   
#test area
#============
getPage()
print("写入完毕，共"+str(book_id)+"篇文章:D")
#============
