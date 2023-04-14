dayup=pow(1.001,365)
daydown=pow(0.999,365)
print("向上千分之一，和向下千分之一")
print("向上：{:.2f} ，向下:{:.2f}".format(dayup,daydown))

dayfactory=0.005
dayup=pow(1+dayfactory,365)
daydown=pow(1-dayfactory,365)
print("dayfatory:%5")
print("向上：{:.2f},向下：{:.2f}".format(dayup,daydown))


