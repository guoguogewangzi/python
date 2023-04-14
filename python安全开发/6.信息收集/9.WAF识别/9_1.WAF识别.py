'''
pip3 install wafw00f
链接：https://github.com/EnableSecurity/wafw00f
利用wafw00f工具识别waf
'''
import subprocess
import re


''''
wafw00f工具的返回信息：提取其中的信息判断是否有waf
b'\r\n                ______\r\n               /      \\\r\n              (  W00f! )\r\n               \\  ____/\r\n               ,,    __            404 Hack Not Found\r\n           |`-.__   / /                      __     __\r\n           /"  _/  /_/                       \\ \\   / /\r\n          *===*    /                          \\ \\_/ /  405 Not Allowed\r\n         /     )__//                           \\   /\r\n    /|  /     /---`                        403 Forbidden\r\n    \\\\/`   \\ |                                 / _ \\\r\n    `\\    /_\\\\_              502 Bad Gateway  / / \\ \\  500 Internal Error\r\n      `_____``-`                             /_/   \\_\\\r\n\r\n                        ~ WAFW00F : v2.1.0 ~\r\n        The Web Application Firewall Fingerprinting Toolkit\r\n    \r\n[*] Checking https://www.baidu.com\r\n[+] Generic Detection results:\r\n[*] The site https://www.baidu.com seems to be behind a WAF or some sort of security solution\r\n[~] Reason: The server header is different when an attack is detected.\r\r\nThe server header for a normal response is "BWS/1.1", while the server header a response to an attack is "Apache",\r\n[~] Number of requests: 7\r\n
'''
def waf(target):                          #判断是否有waf

    #命令行的方式执行，-m:自动到D:\python3.9.1\Lib\site-packages\目录下找wafw00f目录下的main，shell=True:完全模拟shell命令执行
    resp = subprocess.run(["python3","-m","wafw00f.main",f"{target}"],shell=True,capture_output=True)
    r1= re.search(r'The site [a-zA-z]+://[^\s]*[^\r\n]+',resp.stdout.decode())   #提取判断结果信息
    
    if r1 :                                               #如果存在，则输出
        print(r1.group(0))
        r2 = re.search(r'Reason:[^\r\n]+',resp.stdout.decode())          #如果有理由："reason:"，则输出
        if r2:
            print(r2[0])
    

if __name__ == '__main__':
    waf("https://www.baidu.com")
