import requests

from lxml import etree                      #xpath数据提取模块

url='https://s.weibo.com/top/summary'       #设置url目标
headers={'User -Agent':'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1'}                    #设置请求头：UA

html = requests.get(url=url,headers=headers).text        #发送get请求获得,.text获得文本字符串信息
tree=etree.HTML(html)                                   #创建tree对象

lis=tree.xpath('//td[@class="td-02"]/a/text()')         #tree.xpath('规则语法')：取微博热搜数据,返回为列表
for i,li in enumerate(lis,1):                      #enumerate()：每个元素添加索引：1开始，变为了由元组组成列表
    print(i,li)