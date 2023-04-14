'''
备案号查询：
链接：https://beianx.cn/

'''
import requests
import urllib3
from concurrent.futures import ThreadPoolExecutor

from lxml import etree

urllib3.disable_warnings()

def get_link(name):
    url="https://beianx.cn/bacx/"

    url = url+name
    res = requests.get(url,verify=False,timeout=5)
    html = etree.HTML(res.text)
    #如果获取不到，说明浏览器的请求和requests的请求有所区别，需要把requests的请求中的text复制到www.html文件里，获取对应的xpath语法
    link_list = html.xpath('/html/body/div[1]/div/table/tbody/tr/td[4]/a/@href')  
    return link_list

def get_info(link):
    url = "https://beianx.cn" + link
    res = requests.get(url,verify=False,timeout=5)
    html = etree.HTML(res.text)
    site_name = html.xpath('/html/body/div[1]/div/table[2]/tr[1]/td[1]/text()')[0]
    site_domain = html.xpath('/html/body/div[1]/div/table[2]/tr[2]/td[2]/div/a/text()')[:]
    site_home_page = html.xpath('/html/body/div[1]/div/table[2]/tr[2]/td[1]/div/a/text()')[0]
    site_beian = html.xpath('/html/body/div[1]/div/table[2]/tr[1]/td[2]/text()')[0]
    #info = dict(site_name=site_name,site_domain=site_domain,site_beian=site_beian,site_home_page=site_home_page)
    info = f'{str(site_name)} {str(site_domain)} {str(site_home_page)} {str(site_beian)}'

    with open('beian_info.txt','a',encoding='utf-8') as f:
        print(info)
        f.write(info+'\n')




if __name__ == '__main__':
    name = '深圳市腾讯计算机系统有限公司'
    link_list = get_link(name)
    with ThreadPoolExecutor(100) as pool:
        for link in link_list:
            #info = get_info(link)
            pool.submit(get_info,link)