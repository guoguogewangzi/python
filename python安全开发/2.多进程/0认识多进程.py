#应用场景：数据处理，运算比较多时，理由：数据安全，不共享
import multiprocessing
import time

def shopping():
    for i in range(5):
        print("我在购物")
        time.sleep(1)

def game():
    for i in range(10):
        print("我在游戏")
        time.sleep(1)

if __name__ == '__main__':
    p1=multiprocessing.Process(target=shopping)
    p2=multiprocessing.Process(target=game)
    p1.start()
    p2.start()
