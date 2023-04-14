class DemoClass:
    def __init__(self, name):
        self.name = name
        _ = "同志"                         # 无关紧要的名字
        self.__nick__ = name + _

    def getNick(self):
        return self.__nick__


dc1 = DemoClass("老李")
print(dc1.getNick())
print(dc1.__nick__)
