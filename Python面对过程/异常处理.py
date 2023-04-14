try:
    num = eval(input())
    print(num**2)
except NameError:
    print("输入的不是整数")
