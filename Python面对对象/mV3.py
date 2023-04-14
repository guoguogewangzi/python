# import m
#
# print(m._module_var)
# mc = m._module_class(99)
# print(mc.mc_func())
# m._module_func()

from m import *                 #这种方式不能访问：_X
print(_module_var)              #全局变量
mc = _module_class(99)          #类
print(mc.mc_func())
_module_func()                  #函数
