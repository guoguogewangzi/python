class Fuhao:
    money=1000
    def __init__(self):
        self.fz=1

    def run(self):
        print("坐飞机")

    def eat(self):
        print("eat 1")

class Bgirl:
    yanzhi=200

    def __init__(self):
        self.cz=2

    def shoping(self):
        print("shoping `1")
    def like(self):
        print("da am jiang")

    def eat(self):
        print("eat 2")

class Feng(Fuhao,Bgirl):
    def run(self):
        print('坐火车')
        print('我还想')
        super().run()                  #第一类调用父类的方法
        super(Feng, self).run()        #第二种调用父类的方法


f1=Feng()
f1.run()
super(Feng,f1).run()                       #第三种调用父类的方法，在外部


