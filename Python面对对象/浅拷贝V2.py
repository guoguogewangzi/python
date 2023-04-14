ls = ["Python", [1, 2, 3]]
la = ls.copy()
lb = ls[:]
lc = list(ls)
for i in [ls, la, lb, lc]:
    for c in i:
        print(c, id(c), " ", end=" ")
    print(" ", i, id(i))
