with open ("from_f.txt","r")  as fi ,\
        open("to_f.txt","w") as fo :            #with结束后，文件被自动关闭 #with可以包含多个表达式及as
    for line in fi:
        fo.write(line)