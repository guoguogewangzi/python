'''
pip install IPy -i https://pypi.mirrors.ustc.edu.cn/simple/
'''

import IPy
import queue                                  #知识点：第一行：导包：import queue
import threading

ip_c_list=[]
threads=[]
q=queue.Queue()                                                     #知识点：第二行：创建队列对象
def que():                                                     
    for list in open('ip.txt'):
        q.put(list.rstrip('\n'))                                  #知识点：第三行: 生产数据：q.put()

def starts():                                              
    while not q.empty():                                    ##知识点：第四行:队列不为空，q.empty()
        ip = q.get()                                        #知识点：第五行:消费数据：q.get()
        ip_c=IPy.IP(ip).make_net('255.255.255.0')
        if ip_c not in ip_c_list:
            print(ip_c)
            ip_c_list.append(ip_c)
            
threading.Thread(target=que).start()             #新建线程，往队列加数据


for i in range(10):                             #开10个线程，处理队列中的数据
    t=threading.Thread(target=starts)
    threads.append(t)
for i in threads:                               #启动线程
    i.start()
for i in threads:                               #等待线程结束
    i.join()

print(set(ip_c_list))
print('程序结束')

