import json
import nmap
import  subprocess
import queue
import threading
import time

q=queue.Queue()   
threads=[]

def masscan(target):
    info={}
    # cmd=f'masscan {target} -p 22,80,800 -oJ result.json --rate 1000'
    # print(cmd)
    # result=subprocess.run(cmd,shell=True,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    with  open('result.json','r') as f:
        for i in json.load(f):
            if i['ip'] not in info:
                info[i['ip']] = []
                info[i['ip']].append(str(i['ports'][0]['port']))
            else:
                info[i['ip']].append(str(i['ports'][0]['port']))
    return  info

def ip_queue(info):
    for ip in info.keys():
        q.put(ip)

def deal_queue(nm,info):
    while not q.empty():
        ip=q.get()
        port = ''
        for j in info[ip]:
            port += j+','
        port=port[:-1]
        nm.scan(ip,port)
        host_list=nm.all_hosts()#['120.77.38.47']
        for host in host_list:
            print('*' * 100)
            print(host,end='')
            if nm[host].hostname()=='':
                pass
            else:
                print(':'+nm[host].hostname(),end='')
            print('--------'+nm[host].state())
            for port in nm[host].all_tcp():
                print(str(port)+':'+nm[host].tcp(port)['state'],end='')
                if nm[host].tcp(port)['product']=='':
                    print('')
                else:
                    print('------Product:'+nm[host].tcp(port)['product'])

def mn2(info):                #队列优化
    nm=nmap.PortScanner()
    threading.Thread(target=ip_queue,args=(info,)).start()
    
    for i in range(2):
        t=threading.Thread(target=deal_queue,args=(nm,info))
        threads.append(t)
    for i in threads:
        i.start()
    for i in threads:
        i.join()



def mn1(info):
    nm=nmap.PortScanner()                  
    for ip in info.keys():
        port = ''
        for j in info[ip]:
            port += j+','
        port=port[:-1]
        nm.scan(ip,port)
        host_list=nm.all_hosts()#['120.77.38.47']
        for host in host_list:
            print('*' * 100)
            print(host,end='')
            if nm[host].hostname()=='':
                pass
            else:
                print(':'+nm[host].hostname(),end='')
            print('--------'+nm[host].state())
            for port in nm[host].all_tcp():
                print(str(port)+':'+nm[host].tcp(port)['state'],end='')
                if nm[host].tcp(port)['product']=='':
                    print('')
                else:
                    print('------Product:'+nm[host].tcp(port)['product'])



        

info=masscan('120.77.38.47-120.77.38.48')
print(info)


start = time.time()
mn1(info)
end = time.time()
print(end-start)#30.688615798950195

#使用队列
start = time.time()
mn2(info)
end = time.time()
print(end-start)#14.638514995574951

