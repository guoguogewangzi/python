import socket                                             #全连接方式
from  concurrent.futures import ThreadPoolExecutor
import time

from scapy.layers.inet import IP,ICMP,TCP,sr1            #半连接方式

def tcp_scan(ip,port):                                  #方法一：全连接判断端口：有三次握手
    start = time.time()                                  #开始时间
    s = socket.socket()                                  #创建socket对象，默认tcp协议：socket.AF_INET,socket.SOCK_STREAM
    s.settimeout(1)                                #设置超时时间，不然会一直卡在这
    return_code = s.connect_ex((ip,port))                  #这个connect_ex是返回状态码的方法，连接ip,port       
    s.close()                                   #关闭socket对象连接
    if return_code == 0:                            #返回状态码为0表示成功执行，没有报错，连接成功
        print(f'\033[32m{ip}:{port} is open\033[0m')
    # else:
    #     print(f'{ip}:{port} is close')
    end = time.time()-start                              #结束用时
    #print(f'用时:{end}')

def syn_scan(host,port):                                #方法二：半连接判断端口：只接受返回的SYN=1,ACK=1的包（flasg=SA）
    start = time.time()                                 #开始时间
    pkg=IP(dst=host)/TCP(dport=port,flags="S")          #构建包，构建原则：下一层协议()/当前层协议()
    ans = sr1(pkg,timeout=1,verbose=False)              #发包并接收回包，sr1只接收一次响应
    if ans and str(ans['TCP'].flags) == 'SA':           #先判断ans回包是否存在，才进行取值（如果直接取值可能会报错）
        print(f'\033[32m{ip}:{port} is open\033[0m')
    
    end = time.time()-start                              #结束用时
    print(f'用时:{end}')


if __name__ == '__main__':
    ip='175.24.115.4'
    
    # with ThreadPoolExecutor(500) as pool:
    #     for port in range(2**16):
    #         pool.submit(tcp_scan,ip,port)         #全连接调用


    # with ThreadPoolExecutor(200) as pool2:
    #     for port in range(2**16):
    #         pool2.submit(syn_scan,ip,port)          #半连接调用

    tcp_scan(ip,31137)                         #全连接调用
    tcp_scan(ip,65522)                         #全连接调用
    