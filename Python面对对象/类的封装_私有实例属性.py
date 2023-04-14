class DemoClass:
    def __init__(self, name):
        self.__name = name                                  #私有实例属性

    def getName(self):
        return self.__name


dc1 = DemoClass("老王")
dc2 = DemoClass("老李")
print(dc1.getName(), dc2.getName())
print(dc1._DemoClass__name)
print(dc2._DemoClass__name)
