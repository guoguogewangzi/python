import time

s = ""
print("ִ�п�ʼ")
start=time.perf_counter()
for i in range(100, 1000):
    t = str(i)
    if pow(eval(t[0]),3) + pow(eval(t[1]),3) + pow(eval(t[2]),3) == i :
        s += "{},".format(i)
print(s[:-1])
print("{}".format(end=time.perf_counter()-start))
