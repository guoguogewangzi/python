#所以说，多进程多出来的那个子进程会将主进程中的资源（代码）全部复制一份去执行它所执行的函数

import multiprocessing
import time

def test1(num):
    print(num)
    num +=10
    print(num)

if __name__ == '__main__':
    num=0

    print(num,'main')
    p=multiprocessing.Process(target=test1,args=(num,))
    p.start()
    p.join()
    print(num,'main')