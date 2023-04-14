class DemoClass:
    count = 0                      #类属性

    def __init__(self, name, age):
        self.name = name             #实例属性
        self.age = age               #实例属性
        DemoClass.count += 1

dc1 = DemoClass("李四", 12)
dc2 = DemoClass("王五", 13)
print("总数", DemoClass.count,)
print(dc1.name, dc2.name)
