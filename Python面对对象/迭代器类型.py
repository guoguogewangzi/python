class DemoIterator:
    def __init__(self,container):
        self.container = container
        self.salt = len(self.container)

    def __iter__(self):                                 #重载 __iter__()方法
        return self

    def __next__(self):                                 #重载__next__()方法
        self.salt -=1
        if self.salt >=0:
            return self.container[self.salt]
        else:
            raise StopIteration                         #给出结束异常定义StopIteration

di = DemoIterator([1,2,3,4,5,6,7,8])
for i in di:
    print(i,end=', ')



