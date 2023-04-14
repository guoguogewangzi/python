# import socket
#
# udp_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
# udp_socket.sendto(b"--------------------hello--------------------",('127.0.0.1',8081))
# udp_socket.close()

import socket

socket_udp=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)                                   #创建socket连接对象
socket_udp.sendto(b'--------------zhangxin---------------- ',('127.0.0.1',8081))             #发送数据给服务端
#data=socket_udp.recvfrom(1024)                                                               #接收数据
#print(data[0].decode('utf8'))                                                                #显示数据
socket_udp.close()                                                                           #关闭连接
