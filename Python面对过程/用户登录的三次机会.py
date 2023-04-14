n=0
while n<3:
    user=input()
    password=eval(input())
    if user=="Kate" and password==666666:
        print("登录成功！")
        break
    else:
        n=n+1
        if n==3:
            print("3次用户名或者密码均有误！退出程序。")
