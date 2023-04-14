class EmptyClass:  # 建立一个最小空类
    pass


a = EmptyClass()
a.name = "老李"  # 通过增加属性实现对数据被保存
a.age = 50
a.family = {"儿子": "小李", "女儿": "女李"}
print(a.name, a.age, a.family)
print(a.__dict__)
print(type(a.__dict__))