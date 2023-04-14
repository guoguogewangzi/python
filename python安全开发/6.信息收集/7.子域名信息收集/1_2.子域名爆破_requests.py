import  requests

domain='baidu.com'
with open('subnames.txt','r') as f:
    print('子域名有：')
    for i in f.readlines():
        sub=i.rstrip('\n')
        url=sub+'.'+domain
        try:
            req=requests.get('http://'+url)
            print(url)
        except Exception as e:
            pass