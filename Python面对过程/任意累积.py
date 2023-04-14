
def cmul(s):
    sum=1
    for num in eval(s):
        sum=sum*num
    return sum


'''print(cmul(input()))'''



print(eval("cmul({})".format(input())))


