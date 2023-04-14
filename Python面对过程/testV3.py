from tabulate import tabulate

ls = [[1, 2], [2, 3], [2, 4]]
print(tabulate(ls))

a = [('数字1', '数字2', '数字3'), (111, 222, 333), (111, 222, 333)]
print(tabulate(a))
b = [1, 2, 3, 4, 5]
c = {1, 2, 3, 4, 5}
d = "123123123"
print(tabulate(a))
print(tabulate(d))



