try:
    print("请输入整数")
    print(eval(input())**2)
    
    
except:
    print("异常退出")
else:
    print("正常退出")
finally:
    print("finally")
