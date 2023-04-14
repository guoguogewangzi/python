count = 0
def getCounting(a):
    count = 0
    if a != "":

        def doCounting():
            #global count                                #指全局变量
            nonlocal count                              #指上一层变量(getCounting()层)
            count+=1
        doCounting()
    return count


print(getCounting("1"),",",count)
print(getCounting("2"),",",count)
print(getCounting("3"),",",count)