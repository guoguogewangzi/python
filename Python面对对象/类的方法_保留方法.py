class DemoClass:
    count = 0
    def __init__(self,name):
        self.name = name
        DemoClass.count +=1

    def __len__(self):                          #保留方法
        return len(self.name)

dc1=DemoClass("老王")
dc2=DemoClass("小诸葛")
print(len(dc1))                                 #调用保留方法：保留方法名去掉两边__(对象名)
print(len(dc2))                                 #调用保留方法：保留方法名去掉两边__(对象名)

