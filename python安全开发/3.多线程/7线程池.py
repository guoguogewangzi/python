from concurrent.futures  import ThreadPoolExecutor
#import threading
import os ,time


def test(i):
    print(f'------------{i}----------')
    time.sleep(5)


if __name__ == '__main__':

    # list=[]
    # for i in range(60):
    #     t=threading.Thread(target=test,args=(i,))
    #     t.start()
    #     list.append(t)
    # for i in list:
    #     i.join()


    pool=ThreadPoolExecutor(5)                          #知识点，创建线程池
    for i in range(1,21):
        pool.submit(test,i)                             #类似t=threading.Thread(target=test,args=(i,)) 和 t.start()
    pool.shutdown()                                     #关闭线程池

    print('主')



