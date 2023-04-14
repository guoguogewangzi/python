class DemoClass:
    def __init__(self, name):
        self.name = name

    def __del__(self):              # 析构函数
        print("再见", self.name)


dc1 = DemoClass("老王")
del dc1

