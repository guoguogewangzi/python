'''
User-Agent库
链接：https://fake-useragent.herokuapp.com/browsers/0.1.11
'''

from fake_useragent import UserAgent
import requests

proxies = {"http":"http://127.0.0.1:8080","https":"http://127.0.0.1:8080"}


ua = UserAgent()

def generate_header():                                 #每调用一次都随机生成UA并返回
    return {"User-Agent":ua.random}

def query(url):                                        #判断url是否存在
    resp  = requests.get(url,headers=generate_header(),allow_redirects=False,proxies=proxies)    #allow_redirects=False:关闭跳转
    if resp.status_code == 200:
        print(url,"-"*12,resp)


def get_path_dict(domain):                          #加载字典，传参域名，与uri拼接,并返回列表
    dir_list = list()
    with open("dir.txt",'r',encoding='utf8') as f:
        for line in f.readlines():
            line = line.strip()
            if not line.startswith('#'):
                dir_list.append(domain +line)
    return dir_list


if __name__ == '__main__':

    dir_dict = get_path_dict('http://121.37.235.145:8805/')
    for url in dir_dict:
        query(url)