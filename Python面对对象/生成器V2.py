def getValue(max):
    import random
    ls = list(range(10))
    print(ls,end=",")
    for i in range(max):                    #函数中有迭代/循环过程
        yield ls[random.randint(0,9)]       #每次结果以yield方式表达

for i in getValue(10):                      #结合for..in..使用
    print(i)