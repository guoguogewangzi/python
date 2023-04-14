'''
开源cdn识别项目地址:
https://github.com/shmilylty/OneForAll/tree/master/datai
'''


'''
手工方法：
1、多地ping,如果出现不同的ip则使用了cdn
2、如果出现相同ip,查询微步情报，反查域名，如果有多个不同域名，则使用了cdn,不同域名解析为同一个ip，该ip为cdn
'''

import json

from dns import resolver

#方法一(主要)：查询cname记录与字典匹配，如果存在，则为cdn
def query_cname(url):
    rsv = resolver.Resolver()           #创建DNS解析器对象
    #rsv.nameservers=["233.5.5.5"]      #设置dns服务器地址，不设置默认为系统的dns配置
    resp = rsv.resolve(url,'CNAME')     #查询CNAME记录,resp:返回结果
    cname  = list()

    for answer in resp.response.answer:   #resp.response.answer:是一个列表，列表中的每个元素为对象，循环提取每个元素
        for record in answer.items.keys(): #answer.items.keys():answer.items：answer对象中有items（字典）属性.keys()获取字典所有key值;每个key是一个对象
            b_cname = b".".join(record.target[:-1])  #record.target[:-1]:target为可迭代类型对象，target[-1]剔除最后一个元素“.”,返回元组类型,再以字节.:b"."方式拼接在一起，格式为字节
            #或者，可以加上tuple()转换类型，更好理解
            #b_cname = b".".join(tuple(record.target)[:-1])

            cname.append(b_cname.decode())           #解码保存cname列表里
    return cname                                    #返回结果

#方法二：如果我们已知CDN服务商的IP段，那么我们就直接能够判断是否使用了CDN(根据A记录匹配cdn_ip_cidr字典)
def query_ip(url):
    pass

#方法三：CDN的本质上是缓存，如果请求头中有一些关于缓存的配置，可能会存在CDN，可能不准(根据返回头匹配cdn_header_keys字典)
def query_header(url):
    pass

#方法四：大型网络服务商一般都会注册自己的ASN，通过识别ASN我们可以判定使用了ASN(根据ip通过爬虫、接口等查询asn号：唯一的，匹配cdn_asn_list字典)
def query_ip_asn(url):
    pass

def get_cdn_dict():                                                #加载cdn服务商的域名字典
    with open("cdn_cname_info.json",'r',encoding='utf8') as f:
        text = f.read()
        return json.loads(text)



if __name__ == '__main__':

    cdn_dict = get_cdn_dict()
    cname = query_cname('www.baidu.com')
    for c in cname:
        info = cdn_dict.get(c)            #请求的dns获取的cname值作为字典的key取值，
        if info :                         #如果取到，则存在
            print(info)