import time
import multiprocessing
import os

def shopping():
    time.sleep(2)
    print('子进程1 id：',os.getpid(),'父进程id：',os.getppid())  #获取进程id 与父进程id

def game():
    time.sleep(3)
    print('子进程2 id：',os.getpid(),'父进程id：',os.getppid())
    time.sleep(300)

if __name__ == '__main__':
    p1=multiprocessing.Process(target=shopping)
    p2=multiprocessing.Process(target=game)

    print('父进程id：',os.getpid(),'父进程id：',os.getppid())
    p1.start()
    p2.start()