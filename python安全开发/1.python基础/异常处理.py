# try:
#     f=open('1.txt',mode='r',encoding='gbk')
#     f.read()
# except UnicodeDecodeError as e:
#     print("报错信息如下：\n",e,sep='')

class ZhangError(Exception):                           #知识点，利用学过的类的知识，去继承父类Exception
    def __init__(self,*args):
        self.args=args

for i in range(10):
    print(i)
    if i == 5:
        try:                                         #try--except 异常处理
            raise ZhangError('error')                #抛出异常
        except ZhangError as e :
            print(e.args[0])
            break

