
'''
wappalyzer接口方式实现
利用wappalyzer接口
链接：http://api.wappalyzer.com

'''

import requests


headers={'x-api-key':'RzCDunojm87pdBdUafWAgaWiWdSsm9D4aAjVeQoi'}
url='http://api.wappalyzer.com/live/v2/?url=https://www.heitianlab.com&recursive=false'
data = requests.get(url,headers=headers)
print(data.json())