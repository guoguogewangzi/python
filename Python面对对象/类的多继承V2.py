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


class HumanNameClass(NameClass, DemoClass):         #多继承,super（）也按照深度优先、从左至右原则
    def printName(self):
        return super().printName() +  "你好"


dc1 = HumanNameClass("老王")
print(dc1.printName())