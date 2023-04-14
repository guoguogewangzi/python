

import os

def walkFile(file):

    for root,dirs,files in os.walk(file):


        print(root)
        print()
        # #root 表示"当前"正在访问的 "文件夹" 路径
        # print(root) #第一次循环：poc 、第二次循环：poc\Shiro  、第三次循环：poc\Sprint boot

        # #dirs 表示该文件夹下的 "子目录名" list(列表)
        # print(dirs)#第一次循环：['Shiro', 'Sprint boot'] 、第二次循环：[]  、第三次循环：[]

        #files 表示该文件夹下的 "文件" list(列表)
        # print(files)#第一次循环：['poc1.py', 'poc2.py'] 、第二次循环：['shiro1.py', 'shiro2.py']  、第三次循环：['spring2.py', 'sprint1.py']

        #遍历文件
        for f in files:
            print(os.path.join(root,f))


        # #遍历所有的文件夹
        # for d in dirs:
        #     print(os.path.join(root,d)+'---------')

if __name__ == '__main__':
    walkFile('.\\poc')