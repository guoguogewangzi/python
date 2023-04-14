# import socket
# udp_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)  #socket.SOCK_DGRAM：udp协议
# """ 绑定本地的ip和端口，ip可以不用写，表示本地的任何一个ip
# 这里写的端口号必须要和发送数据对方所填写的端口号一致"""
# local_addr=('',8081)
# udp_socket.bind(local_addr)
#
# recv_data = udp_socket.recvfrom(1024)
# print(recv_data[0].decode("utf-8"))
# udp_socket.close()

import socket

socket_udp=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)                      #创建socket连接对象
socket_udp.bind(('',8081))                                                      #绑定端口和ip:ip空，表示本地任何一个ip
data=socket_udp.recvfrom(1024)                                                  #接收数据
#socket_udp.sendto(b'--------123-------',data[1])                               #发送数据给客户端
print(data[0].decode("utf-8"))                                                  #utf-8解码显示数据
socket_udp.close()                                                              #关闭连接