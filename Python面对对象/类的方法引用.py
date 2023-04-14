class DemoClass:
    def __init__(self, name):
        self.name = name

    def lucky(self, salt=0):
        s = 0
        for c in self.name:
            s += (ord(c) + id(salt)) % 100

        return s


dc1 = DemoClass("老李")

print(dc1.lucky(10))
print(DemoClass.lucky(dc1, 10))                         #与上一行等价

lucky = dc1.lucky                                       #类方法的引用
print(lucky(10))                                        #使用这个引用

