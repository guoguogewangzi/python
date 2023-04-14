class DemoException(Exception):
    pass

try:
    raise DemoException()

except:
    print("捕获DemoException异常")