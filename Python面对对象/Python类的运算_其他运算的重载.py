class NewList(list):
    def __format__(self, format_spec):
        "格式化输出，以逗号分隔"
        t = []
        for c in self:
            if type(c) == type("字符串"):
                t.append(c)
            else:
                t.append(str(c))
        return ", ".join(t)


ls = NewList([1, 2, 3, 4])
print(format([1, 2, 3, 4]))
print(format(ls),type(format(ls)))
