from scapy.layers.l2 import Ether,ARP,srp,srp1

def arp(ip):
    #构建包，构包原则，下一层协议()/当前层协议()
    pkg=Ether()/ARP(pdst=ip)

    #发送包，srp1只接收一次响应,verbose:False,关闭显示详细信息，iface:网卡名称
    ans=srp1(pkg,timeout=1,verbose=False)
    
    #判断是否有回包，如果有则存活，反则无
    if ans:                                            
        print(f"{ip} is alive.")
    else:
        print(f'{ip} is dead.')
    

if __name__ == '__main__':
    arp('10.11.53.1')
    #arp('211.31.99.11')
    #arp('175.24.115.4')
    #arp('192.168.111.138')
