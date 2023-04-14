#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time        : 2021/6/30 14:06
# @Author      : Rubicon 
# @File        : scan.py
# @PROJECT_NAME: 安全开发课程
# @Software    : PyCharm


import requests
import json
import urllib3
import time
import os

urllib3.disable_warnings()

apikey = '1986ad8c0a5b3df4d7028d5f3c06e936c852527d4f3b14be5a1be29617a71df2a'
awvs_url = 'https://10.8.0.12:3443'



headers = {"X-Auth": apikey, 'content-type': "application/json"}

def add_task(url=''):         #添加目标
    try:
        data = {"address": url, "description": "testtest", "criticality": "10"}
        response = requests.post(awvs_url + "/api/v1/targets", data=json.dumps(data), headers=headers, timeout=30,
                                 verify=False)
        result = json.loads(response.content)
        print("[INFO]: Task is added successfully, target_id: " + result['target_id'])
        return result['target_id']             #返回target_id
    except Exception as e:
        print('wwwwwwwwwwwwwww:', str(e))
        return

def get_scan_status(scan_id):
    try:
        response = requests.get(awvs_url + "/api/v1/scans/" + str(scan_id), headers=headers, verify=False)
        result = json.loads(response.content)
        status = result['current_session']['status']
        print(status)
        return status
    except Exception as e:
        print(str(e))
        return

def get_scan_url(scan_id):
    try:
        response = requests.get(awvs_url + "/api/v1/scans/" + str(scan_id), headers=headers, verify=False)
        result = json.loads(response.content)
        return result['target']['address']
    except Exception as e:
        print(str(e))
        return

# 生成报告部分
# def generate_report(scan_id):
#     while True:
#         if get_scan_status(scan_id) == "completed":
#             data = {"template_id": "11111111-1111-1111-1111-111111111115",
#                     "source": {"list_type": "scans", "id_list": [scan_id]}}
#             response = requests.post(awvs_url + "/api/v1/reports", data=json.dumps(data), headers=headers, verify=False)   #生成报告
#             # print(response.text)
#             # print(response.headers)
#
#             report_id = response.json()['report_id']   # 获取报告id
#             # print('report_id:',report_id)
#             scan_url = response.json()['source']['description']
#             print(scan_url)
#
#             while True:
#
#                 res = requests.get(awvs_url + '/api/v1/reports/' + report_id, headers=headers, verify=False)
#                 do_address = res.json()['download']     #获取报告下载地址
#                 print('do_address:', do_address)
#                 if do_address == None:
#                     time.sleep(5)
#                 else:
#                     print(do_address[1])
#                     break
#
#
#             report = requests.get(awvs_url+do_address[1], verify=False)
#
#             if (not os.path.exists("reports")):
#                 os.mkdir("reports")
#
#
#             file = "reports/" + scan_url.split('/')[2] + ".pdf"
#
#             if (os.path.exists(file)):
#                 print("[INFO] %s.pdf has generated" % scan_url[7:])
#                 return
#
#             with open(file, "wb") as f:
#                 f.write(report.content)
#             f.close()
#
#             print("[INFO] %s.pdf is generated successfully" % scan_url[7:])
#             break
#         elif get_scan_status(scan_id) == 'failed':
#             print('任务失败，请检查awvs扫描')
#
#         else:
#             time.sleep(10)

def scan(url):             #开始扫描
    target_id = add_task(url)            #获取任务id

    data = {"target_id": target_id, "profile_id": '11111111-1111-1111-1111-111111111111',
            "schedule": {"disable": False, "start_date": None, "time_sensitive": False}}
    try:
        response = requests.post(awvs_url + "/api/v1/scans", data=json.dumps(data), headers=headers, verify=False)
        scan_id = response.headers['Location'][14:]      #获取扫描id
        print("[INFO]: Task is added successfully, scan_id: " + scan_id)
        list_type = ['failed', 'completed', None, 'Failed', 'aborted', 'aborting']  #代表各种扫描状态
        while 1:            #不断的去判断扫描状态
            print(url, get_scan_status(scan_id))     #通过scan_id(扫描id)获取状态
            if get_scan_status(scan_id) in list_type:
                print('%s completed' % url)
                break
            else:
                time.sleep(5)
        # generate_report(scan_id)
    except Exception as e:
        print(str(e))


# with open("url1.txt", encoding='utf-8') as file:
#     date = file.readlines()
#     for i in date:
#         url = i.split('\n')[0]
#         print(url)
#         scan(url)

url = 'https://edu.hetianlab.com'
scan(url)



# 作业： 使用线程池改进awvs脚本，同时对5个目标进行web漏洞扫描。
#尝试用线程池调用awvs,同时对对个目标进行扫描



