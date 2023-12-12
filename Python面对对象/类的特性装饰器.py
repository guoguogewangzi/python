'''
知识点：类的特性装饰器：@property,@.setter

在这个例子中，Rectangle 类有两个私有属性 _width 和 _height，通过 @property 和 @<property_name>.setter 装饰器创建了可读写的属性 width 和 height。width 和 height 属性都有相应的 getter 和 setter 方法，允许我们获取和设置属性的值，并在设置时进行一些逻辑处理。

@property 装饰器用于创建只读属性，而 @<property_name>.setter 装饰器用于创建可写属性，它定义了一个 setter 方法，允许我们在给属性赋值时进行一些逻辑处理。以下是一个例子：
'''

class Rectangle:
    def __init__(self, width, height):
        self._width = width
        self._height = height

    @property                                    #知识点：'@property'系统内置
    def width(self):
        """Getter method for width."""
        return self._width

    @width.setter                              #知识点：'.setter'系统内置
    def width(self, value):
        """Setter method for width."""
        if value > 0:
            self._width = value
        else:
            print("Width must be a positive number.")

    @property                             #知识点：'@property'系统内置
    def height(self):
        """Getter method for height."""
        return self._height

    @height.setter                     #知识点：'.setter'系统内置
    def height(self, value):
        """Setter method for height."""
        if value > 0:
            self._height = value
        else:
            print("Height must be a positive number.")

    @property
    def area(self):
        """Getter method for the area."""
        return self._width * self._height

# 创建 Rectangle 对象
my_rectangle = Rectangle(width=5, height=8)

# 使用 @property 和 @<property_name>.setter 装饰器
print(f"Width: {my_rectangle.width}")  # 调用 getter 方法
print(f"Height: {my_rectangle.height}")  # 调用 getter 方法
print(f"Area: {my_rectangle.area}")  # 调用 getter 方法

# 使用 @<property_name>.setter 装饰器给属性赋值
my_rectangle.width = 10  # 调用 width 的 setter 方法
my_rectangle.height = 4  # 调用 height 的 setter 方法

print(f"Updated Width: {my_rectangle.width}")
print(f"Updated Height: {my_rectangle.height}")
print(f"Updated Area: {my_rectangle.area}")