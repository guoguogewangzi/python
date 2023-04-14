class DemoClass:
    "A Demo Class"
    def __init__(self,name):
        self.name = name
    def getName(self):
        return self.name
dc1 = DemoClass("老王")

print(DemoClass.__dict__)                              #类名访问保留属性
print(dc1.__dict__)                                    #对象名访问保留属性