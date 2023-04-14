import socket

socket_tcp=socket.socket(socket.AF_INET,socket.SOCK_STREAM)        #创建socket对象
socket_tcp.connect(('127.0.0.1',8081))                              #与服务端建立连接

data=input(">>>:").encode("utf-8")
socket_tcp.sendall(data)                                            #发送数据
data=socket_tcp.recv(1024).decode('utf8')                           #接收数据
print(data)                                                         #显示数据
socket_tcp.close()                                                  #关闭连接

