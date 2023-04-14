try:
    A={1,2,3,4}
    print("在集合中移除一个数：")
    A.remove(eval(input()))
    print(A)
except:
  print("不在集合中！")
