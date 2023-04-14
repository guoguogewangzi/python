# #整数
# a=10
# b=a
# c=10
# print(id(a))
# print(id(b))
# print(id(c))                        #c的引用和a的引用相同_不可变对象引用_整数


a="Python计算生态"
b=a
c="Python"
d="计算生态"
e= c + d
f="Python计算生态"

print(id(a))
print(id(b))
print(id(c))
print(id(d))
print(id(e))
print(id(f))