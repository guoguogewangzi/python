ls = ["Python", [1, 2, 3]]
la = ls.copy()
lb = ls[:]
lc = list(ls)

print("ls", id(ls), ls)
print("la", id(la), la)
print("lb", id(lb), lb)
print("lc", id(lc), lc)
