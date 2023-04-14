'''
就是用到的是：wappalyzer指纹识别工具
链接：https://github.com/chorsley/python-Wappalyzer/blob/master/Wappalyzer/data/technologies.json

0、Wappalyzer是使用JS实现的，想要在命令行里面运行，就需要下载Node.js。

1、查看是否安装成功
node -v

2、安装wappalyzer
npm install -g wappalyzer

在npm中安装好wappalyzer之后，可能会出现无法运行的情况,原因是PowerShell默认情况使用Restricted执行策略，不允许任何脚本运行。另外还有两种执行策略1. AllSigned 2. RemoteSigned 从名称上可以猜出，第一个所有带有签名的脚本可以运行，第二是远程脚本需要签名才能够运行。我们这里将执行策略设置为第二种。

3、查看powershell设置
get-executionpolicy

4、set设置，这样脚本在powershell就能执行了
set-executionpolicy remotesigned

5、测试是否能够执行，-P:json格式化输出
wappalyzer https://www.bilibili.com/ -P
'''


import subprocess
import json

#shell=True:完全模拟终端shell


def wappalyzer(url):
    
    #系统shell命令行调用执行命令：wappalyzer http://www.baidu.com
    s = subprocess.run(["wappalyzer",url],shell=True,capture_output=True)   
    output = s.stdout.decode()                          #获得输出结果
    fingeprint = json.loads(output)                     #json转换python的字典类型
    return fingeprint                                   #返回指纹信息（字典）

if __name__ == '__main__':
    url_list = ['http://192.168.111.130']
    for url in url_list:
        fingeprint = wappalyzer(url)                #调用wappalyzer，获取指纹信息（字典）

        print(json.dumps(fingeprint,indent=4))      #字典变字符串类型，格式化输出
        for i in fingeprint["technologies"]:        #取值：name
            print('name:',i["name"])


    