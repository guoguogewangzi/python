import json
import subprocess
import re

from dns import resolver
import requests
from scapy.layers import inet


class Data:
    def __init__(self, subdomain):
        self.subdomain = subdomain
        self.a_record = None
        self.cdn = None
        self.fingerprint = None
        self.is_web = None
        self.has_waf = None
        self.menu = list()

        self.neighbor_ips = None

    def __repr__(self):
        return f"[{self.subdomain}] cdn: {bool(self.cdn)}"


class Scanner:
    def __init__(self, domain):
        self.domain = domain
        self.sub_dict = self.load_dict("dict/subnames.txt")
        self.cdn_dict = self.load_dict("dict/cdn_info.json")
        self.menu_dict = self.load_dict("dict/dir.txt")

        self.rsv = resolver.Resolver()
        self.rsv.lifetime = self.rsv.timeout = 2
        # self.rsv.nameservers = ["8.8.8.8", "223.5.5.5"]

        self.records = list()

    def load_dict(self, path):
        # 加载字典
        with open(path, "r", encoding="utf-8") as f:
            if path.endswith(".txt"):
                line_list = list()
                for line in f.readlines():
                    # 去掉空格和换行
                    line = line.strip()
                    # 去掉注释
                    if line and not line.startswith("#"):
                        line_list.append(line)
                return line_list
            else:
                json_content = f.read()
                return json.loads(json_content)

    def subdomain_brute(self):
        # 遍历字典，查看子域名是否存在
        for sub in self.sub_dict:
            sub_domain = f"{sub}.{self.domain}"
            try:
                answers = self.rsv.resolve(sub_domain)
            except Exception:
                pass
            else:
                print(f"{sub_domain} is exist.")
                data = Data(sub_domain)
                data.a_record = [a.to_text() for a in answers if a]

                self.records.append(data)

    def cdn_identify(self):
        for record in self.records:
            try:
                answers = self.rsv.resolve(record["subdomain"], "cname")
            except Exception:
                pass
            else:
                cdn_address = [a.to_text()[:-1] for a in answers if a]
                # cdn判断
                for address in cdn_address:
                    if self.cdn_dict.get(address):
                        record.cdn = cdn_address

    def fingerprint_identify(self):
        for record in self.records:
            s = subprocess.run(["wappalyzer", "http://" + record.subdomain], shell=True, capture_output=True)
            output = s.stdout.decode()
            fingerprint = json.loads(output)
            record.fingerprint = fingerprint
            # web服务判定
            record.is_web = not bool(re.search(r"error", output))

    def waf_identify(self):
        for record in self.records:
            has_waf = r"\[\*\] The site .* seems to be behind a WAF or some sort of security solution"
            s = subprocess.run(["python", "-m", "wafw00f.main", f"http://{record.subdomain}"], shell=True, capture_output=True)
            output = s.stdout.decode()
            r = re.search(has_waf, output)
            record.has_waf = bool(r)

    def menu_brute(self):
        for record in self.records:
            if not record.is_web:
                continue
            for menu in self.menu_dict:
                try:
                    resp = requests.get("http://" + record.subdomain + menu, allow_redirects=False, timeout=2)
                except Exception:
                    pass
                else:
                    if resp.status_code == 200:
                        record.menu.append(menu)

    def host_discovery(self):
        for record in self.records:
            if not record.cdn:
                for ip in record.ips:
                    a, b = ip.split(".")[:2]
                    targets = [f"{a}.{b}.{c}.{d}" for c in range(1, 255) for d in range(1, 255)]
                    for t in targets:
                        if self.icmp_detect(t):
                            record.neighbor_ips

    def icmp_detect(self, target):
        pkg = inet.IP(dst=target) / inet.ICMP()
        ans = inet.sr1(pkg, timeout=2, verbose=False)
        return bool(ans)

    def flow(self):
        # 子域名 扫描
        self.subdomain_brute()
        # CDN识别
        self.cdn_identify()
        # 指纹识别
        self.fingerprint_identify()
        # waf识别
        self.waf_identify()
        # 目录扫描
        self.menu_brute()

    @classmethod
    def start(cls):
        instance = cls("baidu.com")
        instance.flow()
        return instance


if __name__ == '__main__':
    scanner = Scanner.start()
    print(scanner)