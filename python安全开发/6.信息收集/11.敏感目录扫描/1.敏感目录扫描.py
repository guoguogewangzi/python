import requests

def get_path_dict(domain):                                 #加载uri字典,domain与uri拼接并返回
    dir_list = list()
    with open("dir.txt",'r',encoding='utf8') as f:
        for line in f.readlines():
            line = line.strip()
            if not line.startswith('#'):
                dir_list.append(domain +line)
    return dir_list


if __name__ == '__main__':
    dir_dict = get_path_dict('http://192.168.111.130')     #传参domain:加载uri字典,获得完整url
    for url in dir_dict:
        resp = requests.get(url,allow_redirects=False,verify=False,)    #发包，allow_redirects=False:关闭跳转
        if resp.status_code == 200:                                     #如果200状态码，则判url存在
            print(url)