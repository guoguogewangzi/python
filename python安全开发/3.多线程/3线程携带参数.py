import threading
import time

def shopping(name):
    print(name)
    name='123'
    print(name)


if __name__ == '__main__':

    name='zx'
    print(name,'--------')
    t1=threading.Thread(target=shopping,args=(name,))
    t1.start()
    print(name,'--------')