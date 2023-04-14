import socket
import threading



def send_msg(client):
    while True:
        client.sendall(input(">>>:").encode('utf-8'))



def rev_msg(client):
    while True:
        data = client.recv(1024).decode('utf-8')
        print('\n'+data,end='')


if __name__ == '__main__':
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 8080))

    t1=threading.Thread(target=send_msg,args=(client,))
    t2=threading.Thread(target=rev_msg,args=(client,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()








