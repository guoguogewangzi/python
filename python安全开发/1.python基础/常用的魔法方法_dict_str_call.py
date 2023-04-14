
class Student:
    count=0
    def __init__(self,name,age,gender):
        self.name=name
        self.age=age
        self.gender=gender
        Student.count+=1

    def run(self):
        print(f"{self.name}正在打怪兽")

    def __str__(self):
        return "Class Student 实例化对象"

    def  __call__(self, *args, **kwargs):
        print("对象+()执行这个函数")

p1=Student("张三",18,'男')
p2=Student("李四",18,'男')
p3=Student("王五",18,'男')

print(p1.__dict__)                #执行__dict__()方法
print(p1,type(p1))                         #执行__str__方法

p1()                              #执行__call__方法
print(p1.count)



