from dns import resolver
from concurrent.futures  import ThreadPoolExecutor
import time

count = 0
result = []                             #子域存在列表

def DNS_A(sub_domain,domain):                        #知识点，子域判断
    global count
    rcv = resolver.Resolver()                      #创建DNS解析器对象
    rcv.nameservers = ['114.114.114.114']         #设置dns服务器ip,该dns服务器为阿里云，如果不行，可以更改dns服务器，反复爆破
    #rcv.query()  旧版                            #旧版的dns请求                             
    try:
        resp = rcv.resolve(f"{sub_domain}.{domain}")       #发出dns请求
        
    except :                                        #如果报错，则未能成功解析
        pass

    else:
        count+=1
        print(f"{sub_domain}.{domain} is exist.{count}")            #未报错，则执行else语句
        result.append(f'{sub_domain}.{domain}')
        


def load_dict(file):                                                   
    """加载字典

    Returns:
        列表: 子域名名字组成的列表
    """
    
    with open(file,'r',encoding='utf-8') as f:
        data=[]
        for i in f.readlines():
            i = i.strip()                                #去除每行两边的空格
            if i and not i.startswith('#') :                  #该行存在，且开头不是'#'进行取值
                data.append(i)    
    return data


if __name__ == '__main__':
    
    data = load_dict('subnames.txt')                      #加载子域名名字字典：15000个,保存为data



    start = time.time()                                 #开始时间
    with ThreadPoolExecutor(100) as pool:            #创建线程池对象
        for sub in data:                                #循环遍历data,判断子域是否存在，
            pool.submit(DNS_A,sub,'baidu.com')    #submit()提交任务
    end = time.time()-start                           #结束计时
    print(f'time_all:{end}')                        #输出时间啊：大概4分钟






    print(result)                                   #输出收集的子域




    with open('result.txt','w') as f:             #将结果result写入文件
        for line in result:
            if line != "":
               f.write(line+'\n')

            