'''

split(sep=None,maxsplit=-1)
sep -分隔符，默认为所有的空字符，包括空格，换行(\n)，制表符(\t)等。
maxsplit -分割次数，默认为-1，即分隔所有



课后作业：改进xray_scan脚本，支持同时对多个目标进行扫描，使用 --webhook-output参数，将扫描的结果统一到一个web页面展示
'''

import os
import threadpool

def scan(target_url):
    output_name  = target_url.split('/')[2] + '.html'
    print(output_name)
    cmd = 'C:\\Users\\86188\\Desktop\\python安全工具开发\\6.漏洞探测\\第二期\\tools\\xray_windows_amd64\\xray_windows_amd64.exe webscan --basic-crawler {} --html-output {}'.format(target_url,output_name)
    print(cmd)
    os.system(cmd)


url_list=[]
with  open('url.txt',encoding='utf-8') as file:
    date = file.readlines()
    for i in date:
        if 'http' not in i:
            continue
        #print(i.split()[0])                     #默认为所有空字符，包括空格，换行(\n)，制表符(\t)等
        url = i.split()[0]
        url_list.append(url)
        #scan(url)




#print(url_list)


#线程池，最大同时执行线程数设置为5，超过5的任务开始排队
taskpool = threadpool.ThreadPool(3)
#生成任务请求队列
requests = threadpool.makeRequests(scan,url_list)#注意其中seeds_list是列表
#将任务放到线程池中开始执行
for req in requests:
    taskpool.putRequest(req)

taskpool.wait()