import os

o1=os.path.exists('F:\python study\project\python_ security_tools_development\实例方法.py')
print(o1)

path=os.path.join('F:\python study\project\python_ security_tools_development','123')
print(path)

a=os.path.split(r'F:\python study\project\python_ security_tools_development\实例方法.py')
print(a,type(a))

# os.mkdir('123')

print(os.getcwd())