##fname = input("请输入要打开的文件:")
##fo =open (fname,"r")
##txt=fo.read()
##print(txt)
##
##fo.close()

##fname = input("请输入要打开的文件:")
##fo =open (fname,"r")
##txt=fo.read(2)
##while txt != "":
##    print(txt)
##    txt=fo.read(2)
##
##fo.close()


fname = input("请输入要打开的文件：")
fo = open(fname,"r")
ls=fo.readlines()
print(ls)
for line in ls:
    print(line,end="")
fo.close()


##fname = input("请输入要打开的文件名称：")
##fo= open(fname,"r")
##
##for line in fo:
##    
##    print(line,end="")
##
##fo.close()


##fname = input("请输入要打开的文件名称：")
##fo= open(fname,"r")
##txt = fo.readline()
##while txt !="":
##    print(txt,end="")
##    txt=fo.readline()
##
##fo.close()
