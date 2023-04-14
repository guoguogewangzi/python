import requests
import re

'''
网页的源码中，一般来说会用meta标签标识使用的编码方式。现在绝大部
份的网站，都是使用的utf-8的编码格式。在Python中也默认使用这种格式，
所以当我们获取到这种类型的网页源码时，可以直接使用。但是依旧存在一
些比较特殊的网页，采用的是所在国家的编码格式，比如我国常用的
GB2313/GBK。这个时候我们就需要对获取的数据进行转码处理。
'''

#resp.encoding 从http header中提取响应内容编码（就是提取meta标签标识使用的编码方式，如:<meta charset="UTF-8">）
#resp.apparent_encoding 从内容中分析出的响应内容编码

#例1：
# resp = requests.get("http://www.changsha.gov.cn/")
# print(resp.text)                             #发现输出的文本里的中文是乱码，下一行则利用.content取二进制数据进行对应编码格式解码
# print(resp.content.decode('gbk',errors='ignore'))          #errors='ignore':当编码格式不对时，忽略它(这里的解码格式没找到)


#例2：
resp = requests.get('https://www.51kim.com/')        #发起请求
content = resp.content.decode('utf-8')                  #.content:取二进制数据并解码
result = re.search(r'<.+?>([^\r\n]+?)</.+?>',content)      #(此处获取了title内容)知识点：获取网页具体内容，利用正则re.search()获取指定数据，?:关闭贪婪模式，调试中会被math='字符串'欺骗，字符串显示的不全，需要print(result[0])打印出来查看

print(result[1])                                        #输出提取的数据
print(resp.headers)                                     #resp.headers:取响应头数据,返回为字典类型
print(resp.json())


