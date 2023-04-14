import multiprocessing
import time

def test1(num):
    print(num)
    num.append(2)
    print(num)

if __name__ == '__main__':
    num=[1]

    print(num,'main')
    p=multiprocessing.Process(target=test1,args=(num,))
    p.start()
    p.join()
    print(num,'main')