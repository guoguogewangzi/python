class DemoClass:
    "A Demo Class"

    def __init__(self, name):
        self.name = name

    def getName(self):
        return self.name


dc1 = DemoClass("老王")
print(DemoClass.__doc__, ",", DemoClass.__module__, ",", DemoClass.__class__)  #类名访问保留属性
print(dc1.__doc__, ",", dc1.__module__, ",", dc1.__class__)                    #对象名访问保留属性

print(type(DemoClass))
print(type(dc1))
