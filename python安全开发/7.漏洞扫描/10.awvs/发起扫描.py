'''
发起扫描：
curl -X POST https://127.0.0.1:3443/api/v1/scans -H 'Content-Type: application/json' -H 'Accept: application/json' -H 'X-Auth: API_KEY'


Body parameter
{
"target_id":"",
"profile_id":"",
"report_template_id":"",
"schedule":{
    "disable":true,
    "time_sensitive":true,
    "history_limit":0,
    "start_date":"string",
    "recurrence":"string",
    "triggerable":"false",
},
"max_scan_time":0,
"incremental":false
}



'''
'''
profile_id:扫描类型，以下是对应的值
11111111-1111-1111-1111-111111111112    High Risk Vulnerabilities
11111111-1111-1111-1111-111111111115    Weak Passwords
11111111-1111-1111-1111-111111111117    Crawl Only
11111111-1111-1111-1111-111111111116    Cross-site Scripting Vulnerabilities
11111111-1111-1111-1111-111111111113    SQL Injection Vulnerabilities
11111111-1111-1111-1111-111111111118    quick_profile_2 0 {"wvs":{"profile":"continuous_quick"}}
11111111-1111-1111-1111-111111111114    quick_profile_1 0 {"wvs:"{"profile":continuous_full}}
11111111-1111-1111-1111-111111111111    FUll Scan  1 {"wvs":{"profile":"Default"}}

'''
import urllib3
import requests
import json

urllib3.disable_warnings()

awvs_url='https://192.168.111.136:3443'

apikey='1986ad8c0a5b3df4d7028d5f3c06e936ca29e483499354cc699ddab7c653cb15c'

headers = {"X-Auth": apikey, 'content-type': "application/json"}


def scan(target_id):
    data = {"target_id": target_id,"profile_id":"11111111-1111-1111-1111-111111111111",
    "schedule":{"disable":False,"start_date":None,"time_sensitive":False}}

    try:
        response = requests.post(awvs_url + '/api/v1/scans',data=json.dumps(data),headers=headers,verify=False)
        scan_id = response.headers['Location'][14:]
        print("[INFO]: Task is added successfully,scan_id:"+scan_id)
    except Exception as e:
        print(str(e))


if __name__ == '__main__':
    scan('e1844b4d-1726-475f-953a-2ad36d068b55')