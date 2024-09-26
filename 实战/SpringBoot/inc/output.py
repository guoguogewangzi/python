#内置库
import time,os,sys

#重新开始提示
def logo():
    logo0 = "------开始------"

    print(logo0)

#参数不正确，帮助提示
def usage():
    print('''
用法如下:
        -t header.txt            导入自定义HTTP头部
        -p 127.0.0.1:10809       指定代理(不用怀疑，就是ip+port)
          
        -u http://127.0.0.1      一个url信息泄露扫描
        -uf url.txt              批量url信息泄露扫描
          
        -v http://127.0.0.1      一个url漏洞扫描
        -vf url.txt              批量url漏洞扫描
          
        -d http://127.0.0.1 	 扫描并下载SpringBoot敏感文件
          
        -z key -f key -y key     通过API下载数据
        ''')


