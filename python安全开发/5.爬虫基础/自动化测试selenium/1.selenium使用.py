#chromedriver.exe下载链接：https://chromedriver.storage.googleapis.com/index.html

from selenium import webdriver
import time

wd = webdriver.Chrome('chromedriver/chromedriver.exe')                 #创建 WebDriver 对象，指明使用chrome浏览器驱动
wd.get('https://www.baidu.com')                                        #调用WebDriver 对象的get方法 可以让浏览器打开指定网址
element = wd.find_element_by_id('kw')            #知识点,根据id选择元素，返回的就是该元素对应的WebElement对象(kw:该处为搜索框)
element.send_keys('你好\n')                                            # 在搜索框里发送数据：“你好” ;\n表示:检索
time.sleep(5)
wd.close()                                                             #关闭WebDriver对象


