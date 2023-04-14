'''
pip3 install python-nmap -i https://pypi.mirrors.ustc.edu.cn/simple/ 

重要的两个类：

（1）PortScanner：端口扫描

（2）PortScannerHostDict：用于存储和访问主机扫描结果的特殊小类

'''

import nmap 
import json
nm = nmap.PortScanner()
result = nm.scan('www.baidu.com','22,80')

# print(json.dumps(result,indent=2))

# host_list=nm.all_hosts()
# print(host_list)

'''PortScannerHostDict类使用方法：nm[]'''
# print(json.dumps(nm['192.168.111.130'],indent=2))   #nm['192.168.111.130']:PortScannerHostDict类中通过nm[]来获取值,获取了result其中的scan结果

host_list=nm.all_hosts()#['192.168.111.130']         #获取主机列表            

print(nm[host_list[0]].hostname())#www.baidu.com            #获取域名
print(nm[host_list[0]].state())     #up                  #获取主机状态
print(nm[host_list[0]].all_tcp())#[22, 80]              #获取主机所有端口列表
print(nm[host_list[0]].tcp(22))                         #获取端口信息