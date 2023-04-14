import json
from concurrent.futures import ThreadPoolExecutor

from dns import resolver


class CDN:
    def __init__(self):
        self.rsv = resolver.Resolver()
        self.rsv.timeout = self.rsv.lifetime = 2

        self.cdn_dict = self.get_cdn_dict()

    def query_cname(self, url):
        cname_list = list()
        try:
            resp = self.rsv.resolve(url, "CNAME")
        except Exception:
            pass
        else:
            for answer in resp.response.answer:
                for record in answer.items.keys():
                    b_cname = b".".join(record.target[:-1])
                    cname_list.append(b_cname.decode())
        return cname_list

    @staticmethod
    def get_cdn_dict():
        with open("dict/cdn_info.json", "r", encoding="utf-8") as f:
            text = f.read()
            return json.loads(text)

    def run(self, data):
        """
        :param url: www.zhihu.com
        """
        cdn_dict = self.get_cdn_dict()
        cname_list = self.query_cname(data.subdomain)

        cdn_info_list = list()
        for cname in cname_list:
            cdn_info = cdn_dict.get(cname)
            cdn_info_list.append(cdn_info)
        data.set_cdn(cdn_info_list)

    def mt_run(self, subdomain_data_list):
        with ThreadPoolExecutor() as pool:
            for subdomain_data in subdomain_data_list:
                pool.submit(self.run, subdomain_data)


if __name__ == '__main__':
    cdn = CDN()
    info = cdn.run("www.zhihu.com")
    print(info)
