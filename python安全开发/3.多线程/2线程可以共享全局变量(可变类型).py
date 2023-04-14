import threading
import time

def shopping():
    print(list,id(list))
    list.append(2)
    print("我在逛街")
    time.sleep(1)
    print("我逛完了")
    print(list, id(list))

if __name__ == '__main__':
    list=[1]
    print("-------------\n", list, id(list),'\n----------------')

    t1=threading.Thread(target=shopping)
    t1.start()
    t1.join()
    print("-------------\n",list,id(list),'\n-------------------')
