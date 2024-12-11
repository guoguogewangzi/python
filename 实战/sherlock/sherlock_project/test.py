from requests_futures.sessions import FuturesSession
from time import monotonic
import requests
import urllib3
urllib3.disable_warnings()

#重写request的区别：在请求响应中自动记录响应时间
class SherlockFuturesSession(FuturesSession):

    def request(self, method,url,hooks=None,*args,**kwargs):
        if hooks is None:
            hooks = {}
        start = monotonic()  #时间计时器，起始时间

        def response_time(resp,*args,**kwargs):  
            resp.elapsed = monotonic() - start
            return
        try:
            #判断1：hooks["response"]是否属于list类型
            if isinstance(hooks["response"],list):  
                hooks["response"].insert(0,response_time)# hooks["response"] 列表的开头（索引 0 位置）插入一个元素 response_time
            #判断2：hooks["response"]是否属于元组（tuple）类型
            elif isinstance(hooks["response"],tuple):
                hooks["response"] = list(hooks["response"])#转换为列表（list）类型
                hooks["response"].insert(0,response_time)# hooks["response"] 列表的开头（索引 0 位置）插入一个元素 response_time
            else:
                hooks["response"] = [response_time,hooks["response"]]#比如：hooks["response"] 将变为 [response_time, ['a', 'b', 'c']]
        except KeyError:
            hooks["response"] = [response_time] #hooks["response"] 值被覆盖为:[response_time]

        return super(SherlockFuturesSession,self).request(method,url,hooks=hooks,*args,**kwargs) #与直接super().request()等效，都是调用父类的 request 方法。

cookies={}
url_probe="https://gitea.com/guoguogewangzi"
headers = { "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0",} 
proxy= "http://127.0.0.1:8080"
proxies = {"http":proxy,"https":proxy}
allow_redirects = True
timeout=60
request_payload=None
max_workers = 100

#proxies=proxies,
underlying_session = requests.session()
session = SherlockFuturesSession(max_workers=max_workers,session=underlying_session)
request = session.get
future = request(url = url_probe,headers = headers,proxies=proxies,allow_redirects=allow_redirects,verify=False,timeout=timeout,json=request_payload,cookies=cookies) 


#proxies=proxies,
session2 = FuturesSession(max_workers=max_workers,session=underlying_session)
request2 = session2.get
#future2 = request2(url = url_probe,headers = headers,proxies=proxies,allow_redirects=allow_redirects,verify=False,timeout=timeout,json=request_payload,cookies=cookies) 


#res =requests.get(url=url_probe,headers=headers,proxies=proxies,verify=False,timeout=5)

print("结束！")


