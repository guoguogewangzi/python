def dayday(dayfd):
    dayup=1

    for i in range(365):
        if i%7 in [0,6] :
            dayup=dayup-dayup*0.01
        else:
            dayup=dayup+dayup*dayfd
    return dayup       
#print("运算后：{:.2f}".format(dayup))

factory=0.01
while dayday(factory) < 37.78:
    factory=factory+0.001
print("{:.3f}".format(factory))
