f=open("csv.csv")
ls=[]
for line in f:
    line=line.replace("\n","")
    ls.append(line.split())
    
f.close()
print(ls)

##
##ls=[['你','我','他'],
##    ['毒','是','个'],
##    ['七','恶','他']]
##f=open("1.txt","w")
##for item in ls:
##    f.write(",".join(item)+'\n')
##f.close()
