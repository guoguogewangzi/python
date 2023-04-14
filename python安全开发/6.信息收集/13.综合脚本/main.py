import requests
import time

from jinja2 import Environment, FileSystemLoader

from base.host_discovery import HostDiscovery
from base.port_detect import PortDetect
from base.subdomain_brute import SubdomainBrute
from base.cdn import CDN
from base.fingerprint_identify import FingerprintID


class WebData:
    def __init__(self):
        self.fingerprint = None
        self.has_waf = None
        self.menu = list()


class DomainData(WebData):
    def __init__(self, domain):
        super(DomainData, self).__init__()

        self.subdomain = domain
        self.a_record = None
        self.has_cdn = None
        self.cdn_info = None

        self.neighbor = None

    def set_cdn(self, cdn_info):
        if cdn_info:
            self.has_cdn = True
            self.cdn_info = cdn_info


class IpData(WebData):
    def __init__(self, ip, port):
        super(IpData, self).__init__()

        self.address = f"{ip}:{port}"
        # self.is_web = self.is_web()
        self.is_web = None

    def __repr__(self):
        return f"{ip}:{port}"

    def is_web(self):
        try:
            requests.get("http://" + self.address)
        except Exception:
            pass
        else:
            return True


class Scanner:
    def __init__(self):
        self.host_disc = HostDiscovery()
        self.port_detect = PortDetect()
        self.subdomain_brute = SubdomainBrute()
        self.cdn_detect = CDN()
        self.fingerprint_id = FingerprintID()

    def start_with_domain(self, domain):
        subdomains = list()
        # 子域名爆破
        for subdomain, a_record in self.subdomain_brute.multi_run(domain):
            subdomain = DomainData(subdomain)
            subdomain.a_record = a_record
            subdomains.append(subdomain)

        # cdn检测
        self.cdn_detect.mt_run(subdomains)

        # IP和端口探测
        for subdomain in subdomains:
            if not subdomain.has_cdn:
                for address in subdomain.a_record:
                    neighbor = self.start_with_ip(address)
                    subdomain.neighbor = neighbor
        return subdomains

    def start_with_ip(self, ip):
        data_list = list()
        # for neighbor_ip in self.host_disc.mt_run(ip):
        #     for port in self.port_detect.mt_run(neighbor_ip):
        #         ip_data = IpData(neighbor_ip, port)
        #         data_list.append(ip_data)
        if self.host_disc.icmp_detect(ip):
            for port in self.port_detect.mt_run(ip):
                ip_data = IpData(ip, port)
                data_list.append(ip_data)
        return data_list

    def get_web_info(self, data):
        if isinstance(data, DomainData):
            pass
        elif isinstance(data, IpData):
            # 检查is_web标志
            pass

    def report(self, data):
        """
        生成报告
        """
        template = self.report_env.get_template("test.html")
        res = template.render(data=data)
        with open(f"reports/{str(datetime.now())}.html", "w") as f:
            f.write(res)


def report(data):
    """
    生成报告
    """
    report_env = Environment(
        loader=FileSystemLoader(searchpath="./templates")
    )
    template = report_env.get_template("report.html")
    res = template.render(data=data)
    with open(f"reports/{str(time.time())}.html", "w", encoding="utf-8") as f:
        f.write(res)


if __name__ == '__main__':
    ip = "192.168.29.129"
    data = list()
    for port in range(1, 100):
        for id in range(1, 100):
            ip_data = IpData(ip, port)
            ip_data.is_web = id
            data.append(ip_data)
    report(data)