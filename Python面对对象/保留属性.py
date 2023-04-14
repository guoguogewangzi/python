class DemoClass:
    "A Demo Class"

    def __init__(self, name):
        self.name = name

    def getName(self):
        return self.name


dc1 = DemoClass("老王")
print(DemoClass.__qualname__, DemoClass.__name__, DemoClass.__bases__)          #仅用<类名>访问的保留属性
