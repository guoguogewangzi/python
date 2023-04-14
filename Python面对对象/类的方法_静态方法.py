"""静态方法是类中的函数，不需要实例。静态方法主要是
用来存放逻辑性的代码，主要是一些逻辑属于类，但是
和类本身没有交互，即在静态方法中，不会涉及到类中
的方法和属性的操作。可以理解为将静态方法存在此类
的名称空间中。事实上，在python引入静态方法之前，
通常是在全局名称空间中创建函数"""
class DemoClass:
    count =0
    def __init__(self,name):
        self.name = name
        DemoClass.count +=1
    @staticmethod
    def foo():                          #静态方法：可以用对象方式访问
        DemoClass.count *=100
        return DemoClass.count
dc1= DemoClass("老王")
print(DemoClass.foo())                #调用静态方法：类名.foo() 
print(dc1.foo())                        #调用静态方法：对象名.foo()

