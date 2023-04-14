class DemoClass:
    def __init__(self, name):
        self.name = name

    def lucky(self):                        #实例方法
        s = 0
        for c in self.name:
            s += ord(c) % 100
        return s


dc1 = DemoClass("老王")
dc2 = DemoClass("老李")
print(dc1.name, "的幸运数是：", dc1.lucky())           #调用实例方法：对象名.lucky()
print(dc2.name, "的幸运数是：", dc2.lucky())           #调用实例方法：对象名.lucky()
