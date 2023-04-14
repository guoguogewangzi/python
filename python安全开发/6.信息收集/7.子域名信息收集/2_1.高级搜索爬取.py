'''
利用搜索语法，百度搜索语法，google hacking的url接口搜索对应的语法获取text，正则匹配对应的标签有子域

'''
import re

import requests

domain = 'baidu.com'                 #设置一级目标

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}                        #设置UA

session = requests.session()         ## 创建session对象，获取这一次的cookie等参数
print(session)

# 利用session对象(默认使用该session之前使用的cookie等参数)获取页面源代码,该url：根据搜索引擎搜索site:baidu.com之后生成的url查询接口
resp = session.get(f'https://www.baidu.com/s?wd=site:{domain}',headers = headers)     
 
 #知识点，创建正则实例搜索的时候不用每次都写一遍正则了，用+号拼接，不用f,因为{}在正则里是量词
# regex = re.compile(r'<a.*>(.+).' + domain + r'/</a>')        
# result = regex.findall(resp.text)

result = re.findall(r'<a.*>(.+).' + domain + r'/</a>',resp.text)


print(result)
