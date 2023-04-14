import threading
import time

def shopping():
    print("我在逛街")
    time.sleep(1)
    print('我逛完了')

def game():
    print('我在打游戏')
    time.sleep(1)
    print('我打完了')

if __name__ == '__main__':

    t1=threading.Thread(target=shopping)            #创建线程t1
    t2=threading.Thread(target=game)                #创建线程t2
    t1.start()                                      #开始t1
    t2.start()                                      #开始t2
