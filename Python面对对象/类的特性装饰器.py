class DemoClass:
    def __init__(self, name):
        self.name = name

    @property                           #@property 用于转换方法为属性
    def age(self):
        return self._age

    @age.setter                                     #<方法名>.setter 用于设定属性的赋值操作
    def age(self, value):
        if value < 0 or value > 100:
            value = 30
        self._age = value


dc1 = DemoClass("老李")
dc1.age = -100                                        #会调用def age(self, value)
print(dc1.age)
