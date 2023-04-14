score=eval(input())

if score>=90:
    grade='A'
elif score>=80:
    grade='B'
elif score>=70:
    grade='C'
elif score>=60:
    grade='D'
else:
    print("不合格")
print("你的等级为:{}".format(grade))

