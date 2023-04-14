# la =[]
# lb = la
# lc = []
#
# print(id(la))
# print(id(lb))
# print(id(lc))

la = []
lb = la
lb.append(1)
print(la, id(la))
print(lb, id(lb))
