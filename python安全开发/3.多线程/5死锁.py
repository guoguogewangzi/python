import threading
import time

def run(name):
    mutex1.acquire()                   #1.获得mutex1锁
    print(name+'up')
    time.sleep(1)                      #2.睡眠，交出使用权
    mutex2.acquire()                   #5.无法获得mutex2锁，因为run()1未释放


    print(name+'down')
    mutex2.release()
    mutex1.release()


def run1(name):

    mutex2.acquire()                   #3，获得mutex2锁
    print(name+'up')
    time.sleep(1)                      #4.睡眠，交出使用权
    mutex1.acquire()                   #6.无法获得mutex1锁，因为run()未释放


    print(name+'down')
    mutex1.release()
    mutex2.release()


if __name__ == '__main__':
    mutex1=threading.Lock()
    mutex2=threading.Lock()
    t1=threading.Thread(target=run,args=('Thread-1',))
    t2=threading.Thread(target=run1,args=('Thread-2',))
    t1.start()
    t2.start()
