import requests
import json
import sys

def load_json(path):
    with  open(path) as fp:
        return json.load(fp)

header_list = load_json('cdn_header_keys.json')
data = requests.get('http://www.baidu.com')
headers = dict(data.headers)
result = list(map(lambda x:x.lower(), headers.keys()))

for header in result:
    if header in header_list:
        print('存在CDN:' + header)
        sys.exit(0)
    else :
        if header == result[len(result) -1]:
            print('不存在CDN')
