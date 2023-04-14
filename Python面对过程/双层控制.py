s="PYTHON"
while s !="":
    for c in s:
        print(c,end="")
    s=s[:-1]
print("")

s="PYTHON"
while s !="":
    for c in s :
        if c=="T":
            break
        print(c,end="")
    s=s[:-1]
