import requests


class MenuScanner:
    def __init__(self):
        self.path_list = self.get_path_dict()

    @staticmethod
    def get_path_dict():
        path_list = list()
        with open("../dict/dir.txt", "r", encoding="utf-8") as f:
            for line in f.readlines():
                line = line.strip()
                path_list.append(line)
        return path_list

    def query(self, url):
        resp = requests.get(url, allow_redirects=False)
        if resp.status_code == 200:
            return True

    def run(self, url):
        menu_list = list()
        for path in self.path_list:
            url_path = url + path
            if self.query(url_path):
                menu_list.append(url_path)
        return menu_list


if __name__ == '__main__':
    ms = MenuScanner()
    res = ms.run("http://192.168.29.129:80")
    print(res)
