'''
获取网页内容，提取其中的'href'链接，再请求链接，再提取其中的'href'....,满足目标（比如包含，baidu.com）的域名，则保存

'''

import requests
from bs4 import BeautifulSoup

def request(url):                               #request.get获取文本：content.decode()
    response = requests.get(url)
    html = response.content.decode()
    return html



def parse(html):                                 #提取文本里所有的的href标签里的链接，并保存在links列表
    soup = BeautifulSoup(html,"html.parser")
    links =  [x.get("href") for x in soup.find_all("a")]
    return links


def run(target):
    html = request(target)
    links = parse(html)
    print(links)


if __name__ == '__main__':
    run("https://www.baidu.com")



