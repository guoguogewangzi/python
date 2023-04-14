class DemoClass:
    def __init__(self, name):
        self.name = name

    def __id__(self):
        return len(self.name)

    def lucky(self, salt=0,more=9):
        s = 0
        for c in self.name:
            s += (ord(c) + id(salt)+more) % 100
        return s

dc1=DemoClass("老王")
print(dc1.lucky())
print(dc1.lucky(10))
print(dc1.lucky(10,100))