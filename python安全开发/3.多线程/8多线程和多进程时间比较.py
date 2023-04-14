import multiprocessing
import threading
from time import time
import time

def task1(name):
    print(f'----{name}----')
    time.sleep(2)
    print(f'-----{name}-----')

def task2(name):
    print(f'-----{name}-----')
    time.sleep(2)
    print(f'-----{name}-----')


if __name__ == '__main__':
    # x1 = time.time()
    # p1=multiprocessing.Process(target=task1,args=('p1',))
    # p2=multiprocessing.Process(target=task2,args=('p2',))
    # p1.start()
    # p2.start()
    # p1.join()
    # p2.join()
    # x2 = time.time()
    # print(x2-x1)

    x1=time.time()
    t1=threading.Thread(target=task1,args=('t1',))
    t2=threading.Thread(target=task2,args=('t2',))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    x2=time.time()
    print(f'总共用时{x2-x1}')