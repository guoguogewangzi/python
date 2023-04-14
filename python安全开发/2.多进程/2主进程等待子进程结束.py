import multiprocessing
import time

def shoping():
    print('我在逛街')
    time.sleep(5)
    print("我逛完了")

if __name__ == '__main__':
    p1=multiprocessing.Process(target=shoping )
    p1.start()
    p1.join()                                         #知识点在这，子进程结束之后在执行主进程
    print('t1逛完街了')