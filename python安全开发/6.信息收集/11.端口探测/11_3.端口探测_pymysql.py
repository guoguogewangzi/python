import pymysql
import socket

def connect(host,port):                                              #端口判断
    socket.setdefaulttimeout(3)
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try :
        server.connect((host,port))
        return port
    except :
        print(f"'[-]{port}----close")

    finally:
        server.close()

class mysql:
    def __init__(self,host,user,passwd,target):
        self.host = host
        self.user = user
        self.passwd=passwd
        self.conn=None
        self.cursor=None
        self.connect_creatdb(target)
    
    def connect_creatdb(self,target):
        try:
            self.conn=pymysql.connect(host=self.host,user=self.user,passwd=self.passwd)
        except:
            print('数据库连接失败！！！')

        self.cursor=self.conn.cursor()
        self.cursor.execute('create database if not exists Port_Message;')
        sql='create table if not exists Port_Message' + '.' + '%s(port int);'%target
        self.cursor.execute(sql)
        return True

    def execute(self,target,port):
        sql='insert into Port_Message'+'.'+' %s(port) value (%s)'%(target,port)
        self.cursor.execute(sql)
    
    def close(self):
        self.cursor.close()
        self.conn.close()


def main():
    host = input('输入target:')
    host1=host.replace('.','_')
    port=int(input('输入target_port:'))
    mysql1=mysql('127.0.0.1','root','root',host1)
    mysql1.execute(host1,connect(host,port))                    #默认这里一定会返回一个端口（open）
    mysql1.close()


if __name__ == '__main__':
    main()



