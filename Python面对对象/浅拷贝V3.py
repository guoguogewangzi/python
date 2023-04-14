ls = ["Python",[1,2,3]]
la = ls.copy()
lb = ls[:]
lc = list(ls)
lc[-1].append(4)
print(lc,la)
print(ls,lb)
