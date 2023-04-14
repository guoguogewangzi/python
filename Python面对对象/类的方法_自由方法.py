class DemoClass:
    count =0
    def __init__(self,name):
        self.name = name
        DemoClass.count +=1

    def foo():                          #自由方法 不能用对象方式访问
        DemoClass.count *=100
        return DemoClass.count
dc1= DemoClass("老王")                #实例化
print(DemoClass.foo())               #调用自由方法：类名.foo()

