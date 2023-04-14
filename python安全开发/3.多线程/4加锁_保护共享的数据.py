import threading
import time

def task1():
    global num
    for i in range(1000000):
        mutex.acquire()                      #加锁
        num+=1
        mutex.release()                      #解锁

    print('task1--',num)

def task2():
    global num
    for i in range(1000000):
        mutex.acquire()                       #加锁
        num +=1
        mutex.release()                       #解锁

    print('task2--',num)

if __name__ == '__main__':
    num=0
    mutex=threading.Lock()                   #创建一个锁
    t1=threading.Thread(target=task1)
    t2=threading.Thread(target=task2)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print(num)





