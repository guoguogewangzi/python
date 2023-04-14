class DemoClass:
    count = 0

    def __init__(self, name):              #构造方法
        self.name = name
        DemoClass.count += 1

    def getName(self):                    #实例方法
        return self.name


class HumanNameClass(DemoClass):              #继承
    def printName(self):                   #实例方法
        return str(DemoClass.count) + self.name + "同志"          #对基类属性的使用



dc1 = HumanNameClass("老王")                                    #实例化
print(dc1.getName())                                            #继承了基类的实例方法
print(dc1.printName())                                          #对派生类实例方法的使用
print(isinstance(dc1,DemoClass))                                #dc1对象是否是DemoClass类的对象或子类的对象
print(isinstance(dc1,HumanNameClass))                           #dc1对象是否是HumanNameClass类的对象或子类的对象
print(issubclass(HumanNameClass,DemoClass))                     #HumanNameClass类是否是DemoClass类的子类