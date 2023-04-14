import time

t1 = time.time()
t2 = time.ctime()
t3 = time.gmtime()
t4 = time.localtime()
print(type(t1), t1)
print(type(t2), t2)
print(type(t3), t3)
print(type(t4), t4)
print(time.strftime("%Y-%m-%d %H:%M:%S", t3))
print(time.strftime("%Y-%m-%d %H:%M:%S", t4))
