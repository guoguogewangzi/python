import requests


url='https://gimg2.baidu.com/image_search/src=http%3A%2F%2F2c.zol-img.com.cn%2Fproduct%2F124_500x2000%2F748%2FceZOdKgDAFsq2.jpg&refer=http%3A%2F%2F2c.zol-img.com.cn&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1628214324&t=0d373c47253a087e19e8d2f91a55bb87'

content = requests.get(url).content                #content:获取二进制数据,text：获取文本数据


with open("1.jpg",'wb') as f :                     #写入二进制数据
    f.write(content)
