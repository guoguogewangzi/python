import requests

from lxml import etree                      #xpath数据提取模块

url='https://s.weibo.com/top/summary'       #设置url目标
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0'}                    #设置请求头：UA

cookies = {"SUB":"_2AkMSJiQXf8NxqwFRmfoWzGLqboR0zArEieKketXMJRMxHRl-yT9kqkYGtRB6OaYK-E7pYeSnTZ7wLfz3psJifDbdLcUR;","SUBP":"0033WrSXqPxfM72-Ws9jqgMF55529P9D9WFG7WCjD8L6FaLCJE982RmD;","SINAGLOBAL":"2167887049270.3884.1702538017028;","ULV":"1702538017051:1:1:1:2167887049270.3884.1702538017028:"}


res = requests.get(url=url,headers=headers,cookies=cookies)        #发送get请求获得,.text获得文本字符串信息

html = res.content.decode()

tree=etree.HTML(html)                                   #创建tree对象

lis=tree.xpath('//td[@class="td-02"]/a/text()')         #tree.xpath('规则语法')：取微博热搜数据,返回为列表

#自定义
###########################################################################
#lis = tree.xpath('//*[@id="pl_top_realtimehot"]/table/tbody/tr/td[2]/a')

#for i in range(0,len(lis)) :
#    print(i)
#    print(lis[i].text)
###########################################################################




for i,li in enumerate(lis,1):                      #enumerate()：每个元素添加索引：1开始，变为了由元组组成列表
    print(i,li)