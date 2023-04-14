import random
import requests
from lxml import etree

user_agent=[
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/68.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) '  
    'Gecko/20100101 Firefox/68.0',    
    'Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/68.0'
]

headers={
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
         'Accept-Encoding': 'gzip, deflate',
         'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
         'Cache-Control': 'max-age=0',
         'DNT': '1',
         'Referer': 'https://www.google.com/',
         'User-Agent': random.choice(user_agent),
         'Upgrade-Insecure-Requests': '1',
         'X-Forwarded-For': '127.0.0.'
}

list_result = []

session = requests.session()

for i in range(10):
    url=f'https://www.baidu.com/s?wd=site%3Abaidu.com&pn={i*10}&oq=site%3Abaidu.com&tn=SE_PSStatistics_p1d9m0nf&ie=utf-8&usm=2'        #pn={i*10}代表页数，例如：pn=0：第一页，pn=10：第二页
    s = session.get(url,headers=headers)
    data = etree.HTML(s.text)
    #/html/body/div[2]/div[4]/div[1]/div[3]/div/div/div[1]/div[2]/div/div/a[1]/span
    result=data.xpath("//div[@class='f13 c-gap-top-xsmall se_st_footer user-avatar']/a[1]")      #知识点二：xpath取值更方便
    result=data.xpath("/html/body/div[2]/div[4]/div[1]/div[3]/div/div/div[1]/div[2]/div/div/a[1]/span")
    for i in result:
        try:
            if '/' in i.text:
                list_result.append(i.text.split('/')[0])

        except:
            pass
    print(list_result)

print('-----------------------')
print(list(set(list_result)))                            #set变成集合去重
