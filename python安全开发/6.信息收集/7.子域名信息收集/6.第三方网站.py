'''
第三方网站：直接查询别人的数据库获取结果
https://site.ip138.com/

'''

import requests
import re
import  urllib3

urllib3.disable_warnings()

domain = input('请输入domain:')


#自定义头绕过防护
header={
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
"Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
"Accept-Encoding":"gzip, deflate",
"Connection":"close",
"Cookie":"Hm_lvt_d39191a0b09bb1eb023933edaa468cd5=1627886754; Hm_lpvt_d39191a0b09bb1eb023933edaa468cd5=1627886756; PHPSESSID=lls9r2k534pjba58qn3jn2jh8c",
}
data = requests.get(f'https://site.ip138.com/{domain}/domain.htm',headers=header,verify=False,timeout=5)
list_domain = re.findall('<p>\n<a href="/(.*)/"',data.text)
print(domain+"子域名有：")
for i in  list_domain:
    print(i)



