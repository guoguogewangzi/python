'''
知识点1：os.path.join
组合path与paths，返回一个路径字符串
>>>os.path.join("D:/", "PYE/file.txt")
'D:/PYE/file.txt'

知识点2：会一层一层的拼接
第一次循环：dirpath的值为：.\\blug_plu
第二次循环：dirpath的值为：.\\blug_plu\\__pycache__

'''

import os,sys

path='.\\blug_plu'
pathnames = []

for (dirpath,dirname,filenames) in os.walk(path):
    print(dirpath)
    #print(filenames) #['b.py', 'c.py', 'd.py']
    #print(dirpath) #.\blug_plu
    for filename in filenames:
        if '__pychache' in dirpath:
            pass
        else:
            pathnames +=[os.path.join(dirpath,filename)]   
            #print(pathnames)     #['.\\blug_plu\\b.py','...','...']

for bugfile in pathnames:
    pa = bugfile.split('.')[1].rsplit('\\',1)[0]
    #print(pa)                    #\blug_plu
    script_name = bugfile.split('.')[1].rsplit('\\',1)[1]
    #print(script_name)  #b
    print(sys.path[0]+pa) #f:\python study\project\python安全开发\7.漏洞扫描\__import__()函数\blug_plu
    print(script_name)#b

    sys.path.append(sys.path[0]+pa)  #知识点：需要脚本所在目录的绝对路径
    poc = __import__(script_name)    #知识点：需要脚本名

    poc.bug_check()
