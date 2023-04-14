import socket

socket_tcp=socket.socket(socket.AF_INET,socket.SOCK_STREAM)        #创建socket对象
socket_tcp.bind(("",8081))                                         #绑定ip和端口
socket_tcp.listen(5)                                               #设置监听数量（客户端）
sock,addr= socket_tcp.accept()                                     #等待客户端连接(client.connect())，阻塞,创建连接对象


data=sock.recv(1024).decode("utf-8")                               #接收数据
print(data)                                                        #显示数据
data=input(">>>:").encode("utf-8")
sock.sendall(data)                                                 #发送数据给客户端
sock.close()                                                       #关闭与客户端的连接对象
socket_tcp.close()                                                 #关闭socket对象


