# list={}
# count=0
#
# def student(name,age,gender):
#     global count
#     list[count]={'name':name,'age':age,'gender':gender}
#     count+=1
#
# student('张三',18,'男')
# student('李四',18,'男')
# student('王五',18,'男')
# print(list)
# print(count)
# print(list[0]['name'])                #需要通过编号0访问name


class Student:
    count=0
    def __init__(self,name,age,gender):
        self.name=name
        self.age=age
        self.gender=gender
        Student.count+=1


p1=Student("张三",18,'男')
p2=Student("李四",18,'男')
p3=Student("王五",18,'男')
print(p1.name)                      #可以直接通过name访问
print(Student.count)



