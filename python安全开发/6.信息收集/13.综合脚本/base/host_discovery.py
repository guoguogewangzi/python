from concurrent.futures import ThreadPoolExecutor

from scapy.layers import inet, l2


class HostDiscovery:
    def icmp_detect(self, target):
        pkg = inet.IP(dst=target)/inet.ICMP()
        ans = inet.sr1(pkg, timeout=2, verbose=False)
        if ans:
            print(f"{target} is alive.")
            return True

    def arp_detect(self, target):
        pkg = l2.Ether()/l2.ARP(pdst=target)
        ans = l2.srp1(pkg, timeout=2, verbose=False)
        return bool(ans)

    def on_c_segment(self, source, target):
        """
        判断是不是都在C段上。
        :param source:
        :param target:
        :return:
        """
        return source.split(".")[:2] == target.split(".")[:2]

    def mt_run(self, ip):
        # 扫描C段
        a, b = ip.split(".")[:2]
        targets = [f"{a}.{b}.{c}.{d}" for c in range(1, 255) for d in range(1, 255)]

        with ThreadPoolExecutor(500) as pool:
            future_list = list()
            for t in targets:
                future = pool.submit(self.icmp_detect, t)
                future_list.append((t, future))

        ip_list = list()
        for t, future in future_list:
            if future.result():
                print(f"{t} is alive.")
                ip_list.append(t)
        return ip_list


if __name__ == '__main__':
    host = "192.168.29.1"
    host_disc = HostDiscovery()
    res = host_disc.arp_detect(host)
    if res:
        print(f"{host} is alive.")
