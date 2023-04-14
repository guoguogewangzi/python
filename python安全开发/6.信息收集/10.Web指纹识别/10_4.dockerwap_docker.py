'''
docker web方式实现
部署docker wappalyzer web服务方式获取指纹：
第一步：安装docker版 wappalyzer
systemctl start docker
systemctl status docker
docker search wappalyzer
docker pull hunterio/wappalyzer-api
docker images
docker run -id -p 3434:3000 --name api hunterio/wappalyzer-api
docker ps
'''

import requests
import json

url='http://192.168.111.129:3434/extract?url=https://www.hetianlab.com'         

res = requests.get(url,timeout=5)
result = res.json()
print(json.dumps(result,indent=2))



