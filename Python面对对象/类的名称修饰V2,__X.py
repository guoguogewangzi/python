class DemoClass:
    def __init__(self,name):
        self.name = name
        self.__nick = name + "同志"

    def getNick(self):
        return self.__nick

dc1 = DemoClass("老李")
print(dc1.getNick())
print(dc1._DemoClass__nick)
#print(dc1.__nick)