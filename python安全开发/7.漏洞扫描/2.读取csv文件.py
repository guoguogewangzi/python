import csv

res_file = 'vipkid.com.cn.csv'


url_list=[]

with  open(res_file) as f :
    reader = csv.DictReader(f)

    for i in reader:   
        #i是字典{'id': '355', 'alive': '1', 'request': '1', 'resolve': '1', 'url': 'http://999.vipkid.com.cn', 'subdomain': '999.vipkid.com.cn', 'level': '1', 'cname': 'ali-public-noncore-w...kid.com.cn', 'ip': '39.105.226.119', 'public': '1', 'cdn': '1', 'port': '80', 'status': '200', 'reason': 'OK', ...}                                          
        url_list.append(i['url'])
        print(i['url'])
        with open('3.txt',mode='a',encoding='utf-8') as f:
            f.write(i['url']+'\n')

print(url_list)