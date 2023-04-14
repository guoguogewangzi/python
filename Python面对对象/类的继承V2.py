class DemoClass:
    count = 0

    def __init__(self, name):
        self.name = name
        DemoClass.count += 1

    def getName(self):
        return self.name


class HumanNameClass(DemoClass):              #继承
    def printName(self):
        return str(DemoClass.count) + self.name + "同志"          #对基类属性的使用

dc1 = HumanNameClass("老王")

print(id(dc1),type(dc1))                                #返回dc1的标识，Cpython用内存地址表示,和获得类型
print(id(DemoClass),type(DemoClass))                    #返回DemoClass的标识，Cpython用内存地址表示，和获得类型
dc2=dc1
print(dc1 is DemoClass)                                 #判断dc1和DemoClass的标识是否相等
print(dc1 is dc2)                                       #判断dc1和dc2的标识是否相等
print(type(object),type(type))
