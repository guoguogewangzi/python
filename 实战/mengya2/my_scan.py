#内置库
import os,sys,csv

#第三方库
import threadpool

#自定义模块
from cmdline import cmdlineparser,bug_list, get_ips


#从“参数：文件"中读取目标,返回目标列表
############################################################################################
def file_read(filename):
    url_list = []
    if 'csv' in filename:
        with open(filename) as f:
            reader = csv.DictReader(f)
            for i in reader:
                url_list.append(i['url'])
    else:
        with open(filename,encoding='utf-8') as f:
            date = f.readlines()
            for i in date:
                url = i.split('\n')[0]
                url_list.append(url)
    return url_list
############################################################################################


#即将传入参数：".\\bug_plu",返回bug_plu文件夹下所有文件的路径
############################################################################################
def get_poc_list(file):
    poc_list = []
    for root,dirs,files in os.walk(file):
        for f in files:
            file_path = os.path.join(root,f)
            poc_list.append(file_path)
    return poc_list
############################################################################################



#回调函数（保存bug_check的返回值），第一参数:对应的线程，第二个参数：对应线程执行完的返回值，
############################################################################################
def save_callback(request,result):
    try:
        if result:
            with open('result.txt','a',encoding='utf-8') as f:
                f.write(str(result)+ '\n')
    except:
        pass
############################################################################################



#开始启动poc模块里的插件，目标url_list ,线程数：thread
############################################################################################
def scan(poc,url_list,thread):
    taskpool = threadpool.ThreadPool(thread) #（常规操作）线程池对象
    requests = threadpool.makeRequests(poc.bug_check,url_list,save_callback) #（常规操作）生成任务请求队列，第一个参数：待执行函数，第二个参数：待执行函数里的参数值，第三个参数：（回调函数）某个任务的执行结果被成功返回后，它所对应的线程函数将调用此回调函数，并将任务的执行结果作为参数传递给它。
    for req in requests:                   #（常规操作） 将任务提交给线程池
        taskpool.putRequest(req)
    taskpool.wait()                       # （常规操作）等待所有任务执行完成
############################################################################################



#程序入口
##############################################################################################################
def main():

    args = cmdlineparser()                                 #获取“命令行参数”对象
    type = args.type                                      #获取参数值：调用插件的类型


    #分支1：如果参数bug_list存在，则获取poc列表,最后退出程序
    #############################################################################
    if args.bug_list == True:                             
        poc_list = bug_list(os.path.join(os.path.dirname(__file__), "bug_plu"))
        for i in poc_list:
            print(i)
        sys.exit()         
    #############################################################################
    #分支2：如果没有指定目标文件，则从-u参数中获取目标
    #############################################
    elif args.file == None:
        if '/' in args.url:
            target_list = get_ips(args.url)
        else:
            target_list = []
            target_list.append(args.url)
    #############################################
    #分支3：从文件中获取目标
    #######################################################
    else:
        file_name = args.file
        target_list = file_read(file_name)
    #######################################################


    thread = args.thread                                     #获取参数值：线程数
    poc_list = get_poc_list(os.path.join('.','bug_plu'))     #获取bug_plu文件夹下所有文件的相对路径

    #分支1：如果bug_plu存在，则获取参数值：指定的插件漏洞名称
    ##########################################################
    if args.bug_plu != None:
        poc_name = args.bug_plu
    #分支2:否则，为None
    else:
        poc_name = None
    ##########################################################

    #遍历“bug_plu文件夹下所有文件的相对路径”
    print(poc_list)
    for bug in poc_list:

        #分支1：如果路径中存在'__pycache__'或'pyc'，则pass
        #########################################################################################
        if '__pycache__' in bug or 'pyc' in bug:
            pass
        #分支2：对路径：'.\\bug_plu\\redis\\redis_week.py'，处理
        else:
            script_name = os.path.splitext(os.path.basename(bug))[0]    #获得文件名：'redis_week'
            path = os.path.dirname(bug.split('.')[1])                   #获得路径：'\\bug_plu\\redis'
            sys.path.append(sys.path[0] +path)                 #sys.path增加路径:'F:\\mengya2\\bug_plu\\redis'
            poc = __import__(script_name)                       #动态地导入一个模块，上一行已添加路径。可以找到
            
            #分支1：如果poc_name不为空，即指定了插件漏洞名称
            ###########################################################
            if poc_name !=None: 
                #如果文件名与指定的插件漏洞名称相同，则调用扫描 
                if script_name ==poc_name:
                    print('调用{}插件扫描'.format(script_name))
                    scan(poc,target_list,thread)
            #分支2：如果参数值：调用插件的类型为all 或 获取参数值：调用插件的类型 与 ‘poc.get_vul_info()['type']’相同，则调用扫描
            elif type == poc.get_vul_info()['type'] or type == 'all':
                print('调用{}插件扫描'.format(script_name))
                scan(poc,target_list,thread)
            ###########################################################    
        #########################################################################################
##############################################################################################################


                
if __name__ == '__main__':
    main()
