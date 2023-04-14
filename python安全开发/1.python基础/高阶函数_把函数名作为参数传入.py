


#例子1：
# def sum_num(a, b, f):
#     return f(a) + f(b)
# result = sum_num(-1, 2, abs)
# print(result) # 3

def send_msg():
    print("发消息")

def send_box():
    print("发box")

def send_find():
    print("发find")
#
# 例子3：
# list=[send_msg,
#       send_box,
#       send_find]
# for i in list:
#     i()
#
# #例子2：
# dict={'1':send_msg,
#       '2':send_box,
#       '3':send_find}

while True:
    choice=input("请输入:")

    if choice.upper() =="Q":
        break
    choice = dict.get(choice)
    if not choice:
        print("error")
        continue
    choice()

