#命名空间包：pkg1 和 pkg2
import sys

sys.path+=[r'F:\python study\project\Python面对对象\project1',r'F:\python study\project\Python面对对象\project2'] #添加命名空间包所在路径
import pkg1.m1              #导入  #另外：vscode的黄色警告为vscode IDE未找到pkg1，但是由于在sys.path中添加了路径，运行时：python解释器可以找到,正常运行
import pkg1.m3              #导入

pkg1.m1.mecho("hello")     #引用
pkg1.m3.mecho("world")     #引用




