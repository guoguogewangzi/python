import time
s=""
start=time.perf_counter()
for i in range(1,10):
    for j in range(10):
        for k in range(10):
            if i**3+j**3+k**3==i*100+j*10+k:
                s=s+"{},".format(i*100+j*10+k)
                '''print(i*100+j*10+k,end=",")'''
print(s[:-1])   
print("{}".format(time.perf_counter()-start))
