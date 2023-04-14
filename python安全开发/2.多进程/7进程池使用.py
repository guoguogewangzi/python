from concurrent.futures  import ProcessPoolExecutor
import time
import os

def test(name):
    print(f'我是--{name} ,pid:{os.getpid()}')
    time.sleep(1)


if __name__ == '__main__':
    pool=ProcessPoolExecutor(5)          #创建池子对象,容量：5个进程
    for i in range(16):
        pool.submit(test,i)              #相当于  p2=multiprocessing.Process(target=game) 与p1.start()的结合
    pool.shutdown()                      #关闭进程池
    print("结束！")