#大家在网上可能会看到一些项目使用os.system、os.spawn而不是subprocess。因为前者是Python2时代的模块，现在Python3官方已经推荐使用subprocess作为代替。
import subprocess
import re


def shell(host,port=None):
    #python3.7及以上的捕获输出:capture_output=True
    s = subprocess.run(["nmap",host,'-sV'],capture_output=True)    #subprocess.run()执行命令，列表的形式，capture_output：捕获并输出
   
    #python3.6版本的捕获输出:out变量：stdout=subprocess.PIPE,error变量: stderr=subprocess.PIPE
    #res = subprocess.run(["nmap", "192.168.8.54"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    
    if s.returncode == 0 :
        #print(s.stdout.decode('GBK'))    #获取输出结果，在终端shell输出显示，编码为:"GBK"，因为终端为windows操作系统的终端shell。如果是linux则编:"utf-8"
       
        res = s.stdout.decode('GBK')      #获取输出结果并保存
        r = re.findall(r"(\d+)/tcp[ \t\r\n]+([A-Za-z]+)[ \t\r\n]+([^ \t\r\n]+)[ \r]*([^\r\n]*)",res)          #利用正则匹配,其中两个(\d)([A-Za-z]+)分别代表：取"port"，取"open"
        

        for i in r:
            for j in range(len(i)):
                print(i[j],end=' ')

            print("")

if __name__ == '__main__':
    shell('192.168.111.130')