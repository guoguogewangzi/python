'''
一、什么是装饰器：
装饰器是一种用于修改函数或方法行为的特殊类型的函数。它允许你在不修改原始函数代码的情况下，添加额外的功能或修改函数的行为。

二、什么是语法糖：
语法糖是一种语法上的便利，它不会引入新的功能，而只是提供更方便、更易读的语法。语法糖使得代码更加简洁，并且更符合人们的直觉。

三、chatgpt的解释
在这个例子中，my_decorator 是一个装饰器函数，它接受一个函数 func 作为参数，然后返回一个新的函数 wrapper，该函数在调用原始函数之前和之后打印一些信息。使用装饰器语法 @my_decorator 就相当于将 say_hello 函数传递给 my_decorator 函数，然后将返回的新函数赋值给 say_hello。

这是一个语法糖的例子，因为 @my_decorator 提供了一种简洁的方式来应用装饰器，使得代码更易读

四、理解：
1.定义一个自定义函数（装饰器）
这个函数的作用就是，参数接收函数名，经过处理后，返回新的函数名，相当于装饰器的定义：“不修改原始函数代码的情况下，添加额外的功能或修改函数的行为”

2.使用装饰器，使用已知功能的装饰器，让自己的函数可以灵活的拥有该功能，比如同时拥有预处理以及后处理操作（说白了还是函数复用）

3.调用自己的函数（新的）

五、绝招：

@my_decorator
def say_hello(...)

相当于：

say_hello=my_decorator(say_hello)

'''


# 装饰器定义
def my_decorator(func):
    def wrapper():
        print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.")
    return wrapper

# 使用装饰器
@my_decorator
def say_hello():
    print("Hello!")

# 调用被装饰后的函数
say_hello()
