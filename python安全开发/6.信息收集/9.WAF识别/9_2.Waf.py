import random
import os
import requests
import sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

sys.path.append(os.path.join(os.path.dirname(__file__),'plugins'))

def url(target):
    urls=[]
    with open('default_payloads.lst','r') as f:
        for i in f.readlines():
            urls.append('http://' + target + '/?s='+ i)
    return urls

def  post_data():
    with open('post_strings.lst','r') as f:
        list1=[i.rstrip('\n') for i in f.readlines()]
    with open('post_data.lst','r') as f:
        list2=[i.rstrip('\n') for i in f.readlines()]
    return '{}={}&{}={}'.format(random.choice(list1),random.choice(list2),random.choice(list1),random.choice(list2))

def req(urls):
    user_Agent = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/4.0.5 Safari/531.22.7',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.13+ (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6) AppleWebKit/531.4 (KHTML, like Gecko) Version/4.0.3 Safari/531.4',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A',
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_2; en-au) AppleWebKit/525.8+ (KHTML, like Gecko) Version/3.1 Safari/525.6',
    ]
    headers={'User-Agent':random.choice(user_Agent)}
    for i in urls:
        result = requests.post(i,headers=headers,data=post_data(),verify=False)
        Check_waf(result.text,result.headers,result.status_code)
        if i==urls[len(urls)-1]:
            print('可能不存在waf')


def Check_waf(content,headers,status):
    func_list = []
    for i in os.listdir('./plugins'):
        if not i.startswith('_'):
            if not i.startswith('H'):
                func_list.append(i.split('.')[0])

    for i in func_list:
        a = __import__(i,fromlist=['None'])

        if a.detect(content,headers=headers,status=status)==True:                       #检测点
            print('存在waf ------'+a.__product__)
            sys.exit(0)

if __name__ == '__main__':
    target = input('Input targets:')
    urls=url(target)
    req(urls)
