class DemoClass:
    def __init__(self, name):
        self.name = name

    def __id__(self):
        return len(self.name)

    def lucky(self, salt):
        s = 0
        for c in self.name:
            s += (ord(c) + id(salt)) % 100
        return s

    # def lucky(self, salt):
    #     if type(salt) == int:
    #         return "操作一"
    #
    #     elif type(salt) == str:
    #         return "操作二"
    #
    #     else:
    #         return "操作三"


dc1 = DemoClass("老王")
dc2 = DemoClass("老李")
print(dc1.lucky(10))
print(dc1.lucky("10"))
print(dc1.lucky(dc2))
