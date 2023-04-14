import threadpool
import time


def run_task(task):
    time.sleep(3)
    print(f'finished task: {task}')
    return task

def save_callback(request,result):
    #第一个参数是request,可以访问request.requestID
    #第二个参数是request执行完的结果
    print(request.requestID,result)

def main():
    seeds_list = [1,2,3,4,5,6]
    #线程池，最大同时执行线程数设置为5，超过5的任务开始排队
   
    taskpool = threadpool.ThreadPool(2)
    #生成任务请求队列
    requests = threadpool.makeRequests(run_task,seeds_list,save_callback)#注意其中seeds_list是列表

    #将任务放到线程池中开始执行
    for req in requests:
        taskpool.putRequest(req)
    
    taskpool.wait()


if __name__ == '__main__':
    main()



