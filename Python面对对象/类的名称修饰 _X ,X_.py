class DemoClass:
    def __init__(self,name):
        self.name = name
        self._nick = name + "同志"                #约定内部使用：_nick
        self.class_ = name + "同志"               #约定内部使用，仅为了避免重名：class_
    def getNick(self):
        return self._nick



dc1 = DemoClass("老李")
print(dc1.getNick())
print(dc1._nick)
print(dc1.class_)