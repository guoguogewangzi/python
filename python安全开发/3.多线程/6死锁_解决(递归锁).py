import threading
import time

def run(name):
    mutex1.acquire()
    print(name+'up')
    time.sleep(1)
    mutex2.acquire()
    print(name + 'down')
    mutex1.release()
    mutex2.release()


def run1(name):
    mutex2.acquire()
    print(name+'up')
    time.sleep(1)
    mutex1.acquire()
    print(name+'down')
    mutex1.release()
    mutex2.release()

if __name__ == '__main__':
    # mutex1=threading.Lock()
    # mutex2=threading.Lock()
    mutex2 =mutex1 = threading.RLock()                            #解决点在这

    t1=threading.Thread(target=run,args=('Thread-1',))
    t2=threading.Thread(target=run1,args=('Thread-2',))
    t1.start()
    t2.start()