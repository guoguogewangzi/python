class Student:
    school='幼儿园'
    def __init__(self,name,age):
        self.name=name
        self.age=age

    def play(self):
        print(f'{self.name}在打球')
p=Student('123',123)


p.play()                      #调用方式一
Student.play(p)               #调用方式二


print(p)


