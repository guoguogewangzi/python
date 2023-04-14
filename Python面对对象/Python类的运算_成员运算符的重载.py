class NewList(list):
    def __contains__(self, item):                         #成员运算符的重载
        "各元素算术和也作为成员"
        s = 0
        for c in self:
            s += c
        if super().__contains__(item) or item == s:
            return True
        else:
            return False


ls = NewList([6, 1, 2, 3])
print(6 in ls, 12 in ls)
