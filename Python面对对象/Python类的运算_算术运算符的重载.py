class Newlist(list):
    def __add__(self, other):
        result = []
        for i in range(len(self)):
            try:
                result.append(self[i] + other[i])
            except:
                result.append(self[i])
        return result


ls = Newlist([1, 2, 3, 4, 5, 6])
lt = Newlist([1, 2, 3, 4])
print(ls + lt)
