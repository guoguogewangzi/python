from concurrent.futures import ThreadPoolExecutor

# dnspython
from dns import resolver


class SubdomainBrute:
    def __init__(self):
        self.rcv = resolver.Resolver()
        self.rcv.timeout = self.rcv.lifetime = 1
        self.sub_list = self.get_sub_dict()

    def get_sub_dict(self):
        sub_list = list()
        with open("dict/subnames.txt", "r") as f:
            for line in f.readlines():
                # 去除前后空行和换行符
                line = line.strip()
                # 略过被注释的
                if line and not line.startswith("#"):
                    sub_list.append(line)
        return sub_list

    def query_a_record(self, url):
        try:
            answers = self.rcv.resolve(url)
        except Exception:
            pass
        else:
            print(f"{url} is exist.")
            return [a.to_text() for a in answers if a]

    def run(self, domain):
        subdomains = list()
        for sub in self.sub_list:
            url = f"{sub}.{domain}"
            ips = self.query_a_record(url)
            if ips:
                subdomains.append((url, ips))
        return subdomains

    def multi_run(self, domain):
        with ThreadPoolExecutor(200) as pool:
            future_list = list()
            for sub in self.sub_list:
                url = f"{sub}.{domain}"
                future = pool.submit(self.query_a_record, url)
                future_list.append((url, future))

            subdomains = list()
            for url, future in future_list:
                ips = future.result()
                if ips:
                    subdomains.append((url, ips))
            return subdomains


if __name__ == '__main__':
        s = SubdomainBrute()
        subdomains = s.run("baidu.com")
        print(subdomains)
