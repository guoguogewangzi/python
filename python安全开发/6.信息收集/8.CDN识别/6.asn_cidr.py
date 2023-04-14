import json
import socket
import sqlite3
import sys

def get_B(ip):                                #获取ip的十进制
    ip_list = ip.split('.')
    for i in range(len(ip_list)):
        BX = bin(int(ip_list[i]))               #得到"0b11000000 0b10101000 0b1100 0b1001111"
        ip_list[i] = BX[2:]                     #把0b切掉，得到后面的二进制内容
        if len(ip_list[i]) < 8:                 #如果不满足8位，则不全
            strl = '0'*(8-len(ip_list[i])) + ip_list[i]     #补全0的数量："0" * (8-len() )，然后拼接
            ip_list[i] = strl
    val = "".join(ip_list)                      #将所有的二进制拼接合拢
    return int("0b"+val,base=2)                  #将以合拢的二进制转为十进制，"0b"：代表为二进制数，base=2:代表二进制数

def get_ASN_CIDR(B_0_ip):
    db_dict={}
    conn = sqlite3.connect('ip2location.db')
    cursor = conn.cursor()
    result = cursor.execute(f'SELECT * FROM asn WHERE ip_from<={B_0_ip} AND ip_to >={B_0_ip} LIMIT 1;')
    list1 = result.fetchall()

    cursor.close()
    conn.close()
    print(list1)
    db_dict['CIDR']=list1[0][2]
    db_dict['ASN']='AS' +list1[0][3]
    print(db_dict)
    return db_dict


def CDN_result(db_dict):
    with open('cdn_ip_cidr.json','r') as f:
        cidr = json.load(f)
        print(cidr)
    with  open('cdn_asn_list.json','r') as j:
        asn=json.load(j)
        print(asn)

    if db_dict['ASN'] in asn:
        if db_dict['CIDR'] in cidr:
            print("存在CDN")
    else:
        print('不存在CDN')



if __name__ == '__main__':
    target=input('输入目标：(example:www.baidu.com):')
    data = socket.getaddrinfo(target,'80')
    ip=data[0][4][0]
    B_0_ip = get_B(ip)
    print(B_0_ip)
    db_dict = get_ASN_CIDR(B_0_ip)
    CDN_result(db_dict)