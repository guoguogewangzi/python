
'''
以下逻辑感觉有问题

'''
import sys
import dns.resolver
import json

def load_json(path):         
    with open(path) as fp:
        #如果你要处理的是文件而不是字符串，你可以使用 json.dump() 和 json.load() 来编码和解码JSON数据
        return json.load(fp)              

cname_dict = load_json('cdn_cname_keywords.json')


domain='www.taobao.com'
cname = dns.resolver.resolve(domain,'CNAME')                #
for i in cname.response.answer:
    for  j in i.items:
        result = j.to_text()
names = result.lower().split('.')
for name in names:
    print('name:'+name)
    for keyword in cname_dict.keys():
        print('keyword:'+keyword)
        if keyword in name:
            print('存在CDN  '+ keyword)
            #sys.exit(0)
    if name ==names[len(names) - 1]:
        print('不存在CDN')