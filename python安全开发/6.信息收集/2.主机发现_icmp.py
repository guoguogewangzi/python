from typing import Any
from scapy.layers.inet import IP,ICMP,sr,sr1

def icmp(ip):
    #构包，构包原则：下一层协议()/当前层协议()，虽然iP和icmp在同一层
    pkg=IP(dst=ip)/ICMP()                       #
    
    #发包，sr1只接收一次响应，verbose:False,关闭显示详细信息
    ans=sr1(pkg,timeout=2,verbose=False)        #或ans,unans=sr(pkg,timeout=1,verbose=False)
    
    #判断是否有回包，如果有则存活,反则无
    if ans:
        print(f'{ip} is alive.')
    else:
        print(f'{ip} is dead.')



if __name__ == '__main__':
    #icmp('192.168.111.130')
    #icmp('172.31.50.2')
    #icmp('175.24.115.4')
    icmp('10.10.100.160')