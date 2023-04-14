import random
import requests
from lxml import etree
user_agent= [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/68.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) '
    'Gecko/20100101 Firefox/68.0',
    'Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/68.0']
x_forwarded_for=['39.156.69.79','220.181.38.148','220.181.38.148','180.101.49.12','14.215.177.38']
headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
         'Accept-Encoding': 'gzip, deflate',
         'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
         'Cache-Control': 'max-age=0',
         'DNT': '1',
         'Referer': 'https://www.google.com/',
         'User-Agent': random.choice(user_agent),
         'Upgrade-Insecure-Requests': '1',
         'X-Forwarded-For': '127.0.0.'}
result_list=[]
for i in range(1,10):
    #url=f'https://www.sogou.com/web?query=site:hhtc.edu.cn&page={i}'
    url=f'https://www.sogou.com/web?query=site:szcomtop.com&page={i}'
    s=requests.session()
    data=s.get(url,headers=headers)
    a=etree.HTML(data.text)
    list1=a.xpath("//div[@class='vrwrap']/h3/a/@href")
    for j in list1:
        url1='https://www.sogou.com'+j
        result_list.append(s.get(url1,headers=headers).text.split('/')[2])

print(list(set(result_list)))