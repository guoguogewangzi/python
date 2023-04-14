def fact(n,*b):
    s=1
    for i in range(1,n+1):
        s=s*i
    for item in b:
        print(b)
        s=s*item
        
    return s
print(fact(5,2,2))
