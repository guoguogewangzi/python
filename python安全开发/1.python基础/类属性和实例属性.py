class Student:
    school='幼儿园'
    def __init__(self,name,age):
        self.name=name
        self.age=age

p=Student('123',123)


#类属性:school
Student.school              #正常调用
p.school                    #相当于给对象新增school成员



#实例属性:age
p.age                       #正常调用
Student.age                 #无法调用，报错
