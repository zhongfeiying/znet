#encoding=utf-8
import re
import requests
import urllib2
import datetime
import MySQLdb
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
class Splider(object):
  def __init__(self):
  print u'开始爬取内容...'
  ##用来获取网页源代码
  def getsource(self,url):
  headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2652.0 Safari/537.36'}
  req = urllib2.Request(url=url,headers=headers)
  socket = urllib2.urlopen(req)
  content = socket.read()
  socket.close()
  return content
  ##changepage用来生产不同页数的链接
  def changepage(self,url,total_page):
    now_page = int(re.search('page/(\d+)',url,re.S).group(1))
  page_group = []
  for i in range(now_page,total_page+1):
    link = re.sub('page/(\d+)','page/%d' % i,url,re.S)
    page_group.append(link)
  return page_group
  #获取字内容
  def getchildrencon(self,child_url):
  conobj = {}
  content = self.getsource(child_url)
  soup = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')
  content = soup.find('div',{'class':'c-article_content'})
  img = re.findall('src="(.*?)"',str(content),re.S)
  conobj['con'] = content.get_text()
  conobj['img'] = (';').join(img)
  return conobj
  ##获取内容
  def getcontent(self,html_doc):
  soup = BeautifulSoup(html_doc, 'html.parser', from_encoding='utf-8')
  tag = soup.find_all('div',{'class':'promo-feed-headline'})
  info = {}
  i = 0
  for link in tag:
    info[i] = {}
    title_desc = link.find('h3')
    info[i]['title'] = title_desc.get_text()
    post_date = link.find('div',{'class':'post-date'})
    pos_d = post_date['data-date'][0:10]
    info[i]['content_time'] = pos_d
    info[i]['source'] = 'whowhatwear'
    source_link = link.find('a',href=re.compile(r"section=fashion-trends"))
    source_url = 'http://www.whowhatwear.com'+source_link['href']
    info[i]['source_url'] = source_url
    in_content = self.getsource(source_url)
    in_soup = BeautifulSoup(in_content, 'html.parser', from_encoding='utf-8')
    soup_content = in_soup.find('section',{'class':'widgets-list-content'})
    info[i]['content'] = soup_content.get_text().strip('\n')
    text_con = in_soup.find('section',{'class':'text'})
    summary = text_con.get_text().strip('\n') if text_con.text != None else NULL
    info[i]['summary'] = summary[0:200]+'...';
    img_list = re.findall('src="(.*?)"',str(soup_content),re.S)
    info[i]['imgs'] = (';').join(img_list)
    info[i]['create_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    i+=1
  #print info
  #exit()
  return info
  def saveinfo(self,content_info):
  conn = MySQLdb.Connect(host='127.0.0.1',user='root',passwd='123456',port=3306,db='test',charset='utf8')
  cursor = conn.cursor()
  for each in content_info:
    for k,v in each.items():
    sql = "insert into t_fashion_spider2(`title`,`summary`,`content`,`content_time`,`imgs`,`source`,`source_url`,`create_time`) values ('%s','%s','%s','%s','%s','%s','%s','%s')" % (MySQLdb.escape_string(v['title']),MySQLdb.escape_string(v['summary']),MySQLdb.escape_string(v['content']),v['content_time'],v['imgs'],v['source'],v['source_url'],v['create_time'])
    cursor.execute(sql)
  conn.commit()
  cursor.close()
  conn.close()
if __name__ == '__main__':
  classinfo = []
  p_num = 5
  url = 'http://www.whowhatwear.com/section/fashion-trends/page/1'
  jikesplider = Splider()
  all_links = jikesplider.changepage(url,p_num)
  for link in all_links:
  print u'正在处理页面：' + link
  html = jikesplider.getsource(link)
  info = jikesplider.getcontent(html)
  classinfo.append(info)
  jikesplider.saveinfo(classinfo)
