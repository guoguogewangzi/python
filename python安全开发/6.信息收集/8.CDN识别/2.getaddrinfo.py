'''
手工方法的补充，用python实现；域名解析多个ip则存在cdn
Socket.getaddrinfo()方法是做什么的？
向DNS服务器去请求域名所对应的可用的IP地址
'''
import socket

#返回结果：[(<AddressFamily.AF_INET: 2>, <SocketKind.SOCK_STREAM: 1>, 0, '', ('220.181.38.148', 80)), (<AddressFamily.AF_INET: 2>, <SocketKind.SOCK_STREAM: 1>, 0, '', ('39.156.69.79', 80))]


if len(socket.getaddrinfo('baidu.com','www')) > 1:          #如果返回数据大于1，则返回数据有多个ip，则认定存在CDN
    print("存在CDN")

