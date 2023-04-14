##f=open("f.txt","a")
##f.write("你好世界")
##f.close()



f=open("f.txt","w")
ls=["蠕虫","应急","威胁",123]
f.writelines(ls)
f.close()
