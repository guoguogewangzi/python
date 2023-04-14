'''
死亡3连问：

继承了那些：
回答：
1、继承了属性（包括实例属性，类属性）
2、继承了构造方法
3、继承了实例方法
4、继承了静态方法
5、继承了自由方法(类名方式调用)

不继承那些：
回答：
1、不继承类方法(实际上是可以的)

'''

class Parent:
    fz=3                            #类属性
   
   
    def __init__(self,name,age):
        self.money=1000             #实例属性
        self.name=name              #实例属性
        self.age=age                #实例属性

    def run(self):                  #实例方法
        print(f'我是{self.name}，我有{self.money},我再打高尔服')     #调用了实例属性

p1=Parent("王建林",40)  
print(f'{p1.name}有房子：{p1.fz}')
print(p1.name,p1.money)

class Child(Parent):
    pass
    # def run(self):
    #     print(f'我是{self.name}，我有{self.money},我再打ig')

xiaoming=Child("小明",20)                            #继承了构造方法(也可以重载)，Child类实例化：xiaoming
print(f'{xiaoming.name}有房子：{xiaoming.fz}')       #继承了类属性：fz
print(xiaoming.name,xiaoming.money)                  #继承了实例属性:xiaoming.money,xiaoming.name
xiaoming.run()                                       #继承了实例方法:xiaoming.run()
