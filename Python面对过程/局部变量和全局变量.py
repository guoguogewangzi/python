n,s=10,10
def fact(n):
    global s
    for i in range(1,n+1):
        s*=i
    return s
print(fact(n),s) 
