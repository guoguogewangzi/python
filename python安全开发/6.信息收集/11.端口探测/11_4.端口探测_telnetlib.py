import telnetlib


def connect(host,port):
    server=telnetlib.Telnet()
    try:

        server.open(host,port,timeout=3)
        print(f'[+]{port}----open')
    except Exception as err:
        print(f'[-]{port}----close')
    finally:
        server.close()

def main():
    host=input('输入target_host:')
    port=input('输入target_port:')
    connect(host,port)

if __name__=='__main__':
    main()