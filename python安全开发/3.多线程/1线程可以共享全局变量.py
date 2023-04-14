import threading
import time

def shopping():
    print(a)          #查看a
    global num
    print(num)  #
    num +=1
    print(num)                     #可以修改
    print("我在逛街")
    time.sleep(1)
    print('我逛完了')

if __name__ == '__main__':
    a=1
    num=10
    t1=threading.Thread(target=shopping)            #创建线程t1
    t1.start()                                      #开始t1
    t1.join()
    print("main_num:",num)