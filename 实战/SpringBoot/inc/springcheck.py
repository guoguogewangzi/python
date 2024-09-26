#内置库
import json, sys, hashlib

#第三方库
from termcolor import cprint
import requests, urllib3

urllib3.disable_warnings()

outtime = 10

#实际检查web是否是Spring框架函数
def Spring_Check(url, proxies, header_new):
    cprint("[.] 正在进行Spring的指纹识别", "cyan")
    Spring_hash = "0488faca4c19046b94d07c3ee83cf9d6"
    Paths = ["favicon.ico", "AabyssZG666"]
    check_status = 0
    for path in Paths:
        test_url = str(url) + path
        r = requests.get(
            test_url, timeout=outtime, verify=False, headers=header_new, proxies=proxies
        )
        try:
            content_type = r.headers.get("Content-Type", "")
            if r.text and ("timestamp" in r.text):                     #核心代码：报错内容特征符合Spring特征
                cprint("[+] 站点报错内容符合Spring特征，识别成功", "red")
                check_status = 1
            elif "image" in content_type or "octet-stream" in content_type: #核心代码：是一个图片并且hash为Spring图标，符合Spring特征
                favicon_hash = hashlib.md5(r.content).hexdigest()
                if favicon_hash == Spring_hash:
                    cprint("[+] 站点Favicon是Spring图标，识别成功", "red")
                    check_status = 1
            while check_status == 0:
                cprint("[-] 站点指纹不符合Spring特征，可能不是Spring框架", "yellow")
                check_status = 2
        except KeyboardInterrupt:
            print("Ctrl + C 手动终止了进程")
            sys.exit()
        except Exception as e:
            print("[-] 发生错误，已记入日志error.log\n")
            f2 = open("error.log", "a")
            f2.write(str(e) + "\n")
            f2.close()

#检查web是否是Spring框架入口
def check(url, proxies, header_new):
    header_new = json.loads(header_new)
    if "://" not in url:
        url = str("http://") + str(url)
    if str(url[-1]) != "/":
        url = url + "/"
    try:
        requests.packages.urllib3.disable_warnings()
        r = requests.get(
            url, timeout=outtime, verify=False, headers=header_new, proxies=proxies
        )  # 设置超时6秒
        if r.status_code == 503:
            sys.exit()
        else:
            Spring_Check(url, proxies, header_new)
            return url
    except KeyboardInterrupt:
        print("Ctrl + C 手动终止了进程")
        sys.exit()
    except Exception as e:
        cprint(
            "[-] URL为 " + url + " 的目标积极拒绝请求，予以跳过！已记入日志error.log",
            "magenta",
        )
        f2 = open("error.log", "a")
        f2.write(str(e) + "\n")
        f2.close()
        sys.exit()
