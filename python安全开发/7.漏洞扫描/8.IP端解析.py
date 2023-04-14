'''
pip install netaddr -i https://pypi.mirrors.ustc.edu.cn/simple/ 
'''

from netaddr import IPSet

def get_ips(target):
    try:
        ips=[]
        for ip in IPSet([target]):           #它的格式是有个中括号
            ips.append(str(ip))
        return ips
    except:
        pass

if __name__ == '__main__':
    res = get_ips('192.168.1.1/24')
    print(res)