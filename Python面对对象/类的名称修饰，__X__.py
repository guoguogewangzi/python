class DemoClass:
    def __init__(self,name):
        self.name = name
        self.__nick__ = name + "同志"                 #正常的属性名称

    def getNick(self):
        return self.__nick__

dc1 = DemoClass("老李")
print(dc1.getNick())
print(dc1.__nick__)