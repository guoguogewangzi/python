'''
awvs接口

user信息接口
curl -X GET https://192.168.111.136:3443/api/v1/users -H 'Accept: application/json' -H 'x-Auth: 1986ad8c0a5b3df4d7028d5f3c06e936ca29e483499354cc699ddab7c653cb15c' --insecure

目标信息接口
curl -X GET https://192.168.111.136:3443/api/v1/targets -H 'Accept: application/json' -H 'x-Auth: 1986ad8c0a5b3df4d7028d5f3c06e936ca29e483499354cc699ddab7c653cb15c' --insecure


'''

import requests
import json
import urllib3
import time
import os

urllib3.disable_warnings()


apikey='1986ad8c0a5b3df4d7028d5f3c06e936ca29e483499354cc699ddab7c653cb15c'

awvs_url='https://192.168.111.136:3443'

headers = {'X-Auth':apikey,'content-type':'application/json'}

def add_task(url=''):
    try:
        data = {
            "address":url,
            "description":"testtest",
            "criticality":10
            }
        response = requests.post(awvs_url+'/api/v1/targets',data=json.dumps(data),headers=headers,timeout=30,verify=False)
        result = json.loads(response.content)
        print(json.dumps(result,indent=2))
        print("[INFO]: Task is added successfully,target_id: " +result['target_id'])

    except Exception as e:
        print('wwwwwwwwwwwwwww',str(e))
        return

if __name__ == '__main__':
    add_task(awvs_url)



