class DemoClass:
    def __init__(self, name):
        self.name = name

    def printName(self):
        return self.name


class NameClass:
    def __init__(self, title):
        self.nick = title

    def printName(self):
        return self.nick + "同志"


class HumanNameClass(DemoClass, NameClass):         #多继承
    pass


dc1 = HumanNameClass("老王")
print(dc1.printName())
