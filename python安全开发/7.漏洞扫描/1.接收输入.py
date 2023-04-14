import argparse,sys

def Cmdlineparser():
    #使用argparse 的第一步是创建一个ArgumentParser对象，ArgumentParser对象包含将命令行解析成Python数据类型所需的全部信息
    parser = argparse.ArgumentParser(description='Powered by Pghook',
                                    usage='python My_scanT.py -f sub_domain.txt -t 10',
                                    add_help=True)

    parser.add_argument('-u','--url',help='指定要扫描目标url')
    parser.add_argument('-f','--file',help='从文件中读取扫描目标')
    parser.add_argument('-t','--thread',type=int,help='扫描线程设置',default=1)
    parser.add_argument('-b','--bug_plu',help='指定漏洞插件名称')
    parser.add_argument('-bl','--bug_list',default='False',action='store_true',help='列出漏洞插件列表')   #action='store_true':只需要-bl 不需要值，默认值为False,如果使用了-bl参数，值则为True
    if len(sys.argv)==1:
        sys.argv.append('-h')
    return parser.parse_args()

def main():
    args = Cmdlineparser()         #得到的是对象
    print('-u',args.url)
    print('-f',args.file)
    print('-t',args.thread)
    print('-b',args.bug_plu)
    print('-bl',args.bug_list)


if __name__ == '__main__':
    main()




                                