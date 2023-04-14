class DemoClass:
    count =0
    def __init__(self,name):
        self.name = name
        DemoClass.count +=1

    @classmethod
    def getChrCount(cls):                   #类方法
        s = "零一二三四五六七八九多"
        return s[DemoClass.count]           #或 return s[cls.count]
dc1=DemoClass("老王")
dc2=DemoClass("老李")
print(dc1.getChrCount())                 #调用类方法：对象名.getChrCount()
print(DemoClass.getChrCount())            #调用类方法：类名.getCHrCount()
