class DemoClass:
    count = 0

    def __init__(self, name):
        self.name = name
        DemoClass.count += 1

    def printCount(self):
        return str(DemoClass.count) + self.name


class HumanNameClass(DemoClass):
    def __init__(self, name):
        self.name = name

    def printCount(self):
        return super().printCount() + "同志"              # 方法重载_增量重载


dc1 = HumanNameClass("老王")
print(dc1.printCount())
