class DemoClass:
    def __init__(self,name):
        self.name = name

    def __enter__(self):                                #重载__enter__()方法
        print("进入上下文管理器")
        return self                                     #as 引用是__enter__()返回值

    def __exit__(self, exc_type, exc_val, exc_tb):      #重载__exit__方法
        print("退出上下文管理器")


    def run(self):
        print("DemoClass的某个实例对象在运行")


with DemoClass('Python123') as d:                       #as 引用是__enter__()返回值
    d.run()

