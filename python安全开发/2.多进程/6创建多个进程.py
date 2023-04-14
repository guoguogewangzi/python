import multiprocessing
import time


def test(name):
    print(f"我是{name}")
    time.sleep(1)


if __name__ == '__main__':
    p_all=[]
    for i in range(10):
        p=multiprocessing.Process(target=test,args=(i,))
        p.start()
        p_all.append(p)

    for i in p_all:
        i.join()

    print('结束')