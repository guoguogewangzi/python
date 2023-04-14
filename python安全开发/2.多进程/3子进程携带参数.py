import multiprocessing
import time

def test(*args,**kwargs):
    print(args)
    print(kwargs)
if __name__ == '__main__':
    p1=multiprocessing.Process(target=test,args=(1,2,3),kwargs={'13':'123','qwe':'qwe'})
    p1.start()

