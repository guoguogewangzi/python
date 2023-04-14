def fact(n,m=1):
    s=1
    for i in range(1,n+1):
        s=s*i
    return s//m


print(fact(5,5))
