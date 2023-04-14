'''
pip3 install python-masscan -i https://pypi.mirrors.ustc.edu.cn/simple/
subprocess.run(['masscan','127.0.0.1','-p 22,80','--max-rate','1000','--wait','0'])
'''


import masscan
import subprocess
import json

server = masscan.PortScanner()


server.scan('14.215.177.39','80',arguments='--max-rate 1000 --wait 0')
print(json.dumps(server.scan_result,indent=2))
host_list=server.all_hosts
print(host_list)
for host in host_list:
    print(host +'----',end='')
    for port in server.scan_result['scan'][host]['tcp'].keys():
        print(str(port)+':'+server.scan_result['scan'][host]['tcp'][port]['state']+'\t',end='')
        if not server.scan_result['scan'][host]['tcp'][port]['services']:
            print('Services:Unkown')
        else:
            print('Services: '+server.scan_result['scan'][host]['tcp'][port]['services'])




