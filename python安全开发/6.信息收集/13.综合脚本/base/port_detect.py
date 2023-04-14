import socket
from concurrent.futures import ThreadPoolExecutor


class PortDetect:
    def __init__(self):
        self.port_range = range(1, 9001)

    def socket_detect(self, ip, port):
        s = socket.socket()
        s.settimeout(2)
        try:
            s.connect((ip, port))
        except Exception as e:
            pass
        else:
            print(f"{ip}:{port} is open.")
            return True

    def run(self, ip):
        port_list = list()
        for port in self.port_range:
            if self.socket_detect(ip, port):
                port_list.append((ip, port))
        return port_list

    def mt_run(self, ip):
        with ThreadPoolExecutor(500) as pool:
            future_list = list()
            for port in self.port_range:
                future = pool.submit(self.socket_detect, ip, port)
                future_list.append((port, future))

        port_list = list()
        for port, future in future_list:
            if future.result():
                port_list.append(port)
        return port_list


if __name__ == '__main__':
    host = "192.168.29.129"
    ps = PortDetect()
    res = ps.run(host)
    print(res)
