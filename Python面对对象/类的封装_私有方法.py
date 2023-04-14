class DemoClass:
    def __init__(self, name):
        self.__name = name

    def __getName(self):                    #私有方法
        if self.__name != "":
            return self.__name
        else:
            return "老张"

    def printName(self):
        return "{}同志".format(self.__getName())


dc1 = DemoClass("老王")
dc2 = DemoClass("")
print(dc1.printName(), dc2.printName())
print(dc1._DemoClass__getName(),dc2._DemoClass__getName())
