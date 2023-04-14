class DemoClass:
    __count = 0  # 私有类属性

    def __init__(self, name):
        self.name = name
        DemoClass.__count += 1

    @classmethod
    def getCount(cls):
        return DemoClass.__count


dc1 = DemoClass("老王")
dc2 = DemoClass("老李")
print(DemoClass.getCount())
