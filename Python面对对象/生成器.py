def getValue():
    import random
    ls = list(range(10))
    print(ls, end=",")
    return ls[random.randint(0, 9)]


for i in range(10):
    print(getValue())
