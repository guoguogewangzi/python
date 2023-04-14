#定义一个类，这个类有列表所有属性和方法，但只能添加字符串

class Mylist(list):
    def append(self,obj) -> None:
        if type(obj) == str:
            super().append(obj)


#类似list([1,2,3,4,5,6])创建一个列表
l1=Mylist([1,2,3,4,5,6,'1'])
print(l1)

#添加字符串'2'，添加成功
l1.append('2')
print(l1)

#添加数字0,未添加成功
l1.append(0)
print(l1)