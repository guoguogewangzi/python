import requests
from lxml import etree
from requests.sessions import ContentDecodingError
import threading
from concurrent.futures  import ThreadPoolExecutor
import time

url='https://www.tukuwa.com/'                 #设置url目标

headers={'User -Agent':'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1'}             #设置请求头：UA


html = requests.get(url=url,headers=headers).text     #get请求资源，.text:取响应体文本信息
tree = etree.HTML(html)                                                     #创建tree对象，待使用tree.xpath()取数据
list1 = tree.xpath('//div[@class="wb_ppic"]//img/@src')        #tree.xpath('语法规则')：取图片的url数据(缩略图)，并返回列表
num=0

#老师的
for i,li in list(enumerate(list1)):                           #遍历列表，enumerate()：每个元素添加索引，变为了由元组组成列表,
        new_li=li.replace('pic_360','pic_source')                     #替换url数据中的部分值，url变为原图的url
        content = requests.get(url=new_li,headers=headers).content      #get请求资源，.content:取二进制数据信息
        with open(f'./img/{i}.jpg','wb') as f:                         #'wb'：写入文件，在pthon中写入文件就是下载文件
                f.write(content)
        print(i,'写入完成')


#自己写的
# def download(*args):
#         new_li=args[0]
#         i=args[1]
#         #name:文件名
#         name = new_li.split('/')[-1].replace('.jpg','')
#         print(name)
#         #开始下载
#         content = requests.get(url=new_li,headers=headers).content
#         with open(f'./img/{name}.jpg','wb') as f:
#                 f.write(content)


# pool = ThreadPoolExecutor(30)
# for i,li in enumerate(list1):
#         #new_li：链接
#         new_li=li.replace('pic_360','pic_source')
#         pool.submit(download,new_li,i)
# pool.shutdown()

# print('-----------------结束-----------------------')





#https://up.tukuwa.com/2021/pic_360/3a/ac/1b/3aac1b465831fc5829ff77e533bb2137.jpg #缩略图
#https://up.tukuwa.com/2021/pic_source/3a/ac/1b/3aac1b465831fc5829ff77e533bb2137.jpg #原图

#https://up.tukuwa.com/2021/pic_360/3d/1e/d7/3d1ed78be44d0010714d088d47767ed9.jpg #缩略图
#http://up.tukuwa.com/2021/pic_source/3d/1e/d7/3d1ed78be44d0010714d088d47767ed9.jpg #原图