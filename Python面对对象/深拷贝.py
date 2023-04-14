import copy

ls = ["Python", [1, 2, 3]]

lt = copy.deepcopy(ls)
for i in [ls, lt]:
    for c in i:
        print(c, id(c), " ", end=" ")
    print(" ", i, id(i))




