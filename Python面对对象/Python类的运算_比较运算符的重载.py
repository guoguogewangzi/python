class NewList(list):
    def __lt__(self, other):
        "以各元素算术和为比较依据"
        s, t = 0, 0
        for c in self:
            s += c
        for c in other:
            t += c

        return True if s < t else False


ls = NewList([6, 1, 2, 3])
lt = NewList([1, 2, 3, 99])
print([6, 1, 2, 3] < [1, 2, 3, 99])
print(ls < lt)
