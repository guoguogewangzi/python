import subprocess
import os

# cmd='whoami'

# result=subprocess.run(cmd,shell=True,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)  #shell=True ,调用cmd执行命令
# print(result.stdout)
# print(result.returncode)  #返回状态码：0,1   0：正确执行命令， 1：执行命令有错误

# cmd = ['whoami']
# result=subprocess.run(cmd,shell=False,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)   #shell=False,调用os模块执行命令
# print(result.stdout)

cmd = 'whoami'
result=subprocess.Popen(cmd,shell=True,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
print(result.stdout.read())