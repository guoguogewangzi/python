from selenium import webdriver

import time

wd=webdriver.Chrome('chromedriver/chromedriver.exe')                  #创建 WebDriver 对象，指明使用chrome浏览器驱动
wd.get('https://s.weibo.com/top/summary')                             #调用WebDriver 对象的get方法 可以让浏览器打开指定网址

element=wd.find_elements_by_xpath('//td[@class="td-02"]/a')              #知识点，xpath获取对应数据对象

for i in element:
    print(i.text)                                                       