import socket
import threading
"""
实现服务端和客户端之互发消息
"""


def send_msg(sock):
    while True:
            sock.sendall(input(">>>:").encode('utf-8'))


def rev_msg(sock):
    while True:
            data= sock.recv(1024).decode('utf-8')
            print('\n'+data,end='')


if __name__ == '__main__':
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('', 8080))
    server.listen(5)
    sock, addr = server.accept()
    t1 = threading.Thread(target=rev_msg, args=(sock,))
    t2 = threading.Thread(target=send_msg, args=(sock,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    















