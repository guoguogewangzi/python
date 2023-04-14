from dns import resolver
import json


class Data:                                 #面对复杂的情况，单独创建一个数据类去管理数据
    def __init__(self,subdomain):
        self.subdomain = subdomain
        self.ips = None
        self.cdn = None

    def to_text(self):
        return f"[{self.subdomain}] ips_length: {len(self.ips)} cdn: {bool(self.cdn)}"

    def set_cdn(self):                              #可以创建一个设置属性值的方法，通过self.方式规范属性的值
        pass

    #debug显示时：更改<__main__.record object at 0x0000031231345F>为以下字符串(优先级比str更高的),调用方式：print(record)
    def __repr__(self):
        return f"[{self.subdomain}] ips_length: {len(self.ips)} cdn: {bool(self.cdn)}"



class Scanner:
    def __init__(self,domain):
        self.domain = domain                                          #类型：字符串
        self.sub_dict = self.load_dict("0.dict/subnames.txt")         #类型：列表
        self.cnd_dict = self.load_dict("0.dict/cdn_cname_info.json")  #类型：字符串

        self.rcv = resolver.Resolver()                        #类型：类对象;创建DNS解析器对象
        self.rcv.lifetime = self.rcv.timeout = 2              #设置：lifetime:发起请求到获取回包的时间,timeout:等待响应的时间
        #self.rcv.nameservers = ['114.114.114.114','8.8.8.8']   

        self.records = list()       #类型：列表

    @staticmethod                  #没有用到self，所以加@staticmethod  ，成为静态方法：类中的一个普通函数，由类对象和实例对象共享
    def load_dict(path):
        #加载字典
        with open(path,'r',encoding='utf-8') as f:
            if path.endswith(".txt"):

                line_list = list()
                for line in f.readlines():
                    line = line.strip()
                    if line and not line.startswith('#'):
                        line_list.append(line)
                return line_list
           
            else:
                json_content = f.read()
                return json.loads(json_content)

    def subdomain_brute(self):
        #遍历字典：查看子域名是否存在

        for sub in self.sub_dict:                             #知识点：取属性self.sub_dict
            subdomain = f"{sub}.{self.domain}"

            try:
                answers = self.rcv.resolve(subdomain)        #发起dns请求
            except Exception:
                pass
            else:
                print(f"{subdomain} is exist.")
                data = Data(subdomain)
                data.ips = [ a.to_text() for a in answers if a]  
                self.records.append(data)
                
                '''
                records:[{'subdomain': 'home.baidu.com', 'ips': ['111.206.209.69', '183.232.232.54', '180.101.49.156']}]
                '''
                # self.records.append(dict(                       #records存储A记录查询结果，records是列表，元素是字典
                #     subdomain = subdomain,
                #     ips=[ a.to_text() for a in answers if a]  
                # ))  


    def cdn_identify(self):
        for record in self.records:
            try:
                answers = self.rcv.resolve(record["subdomain"],"CNAME")
            except Exception:
                pass
                #record["cdn"] = False
            else :
  
                cdn_address = [a.to_text()[:-1] for a in answers if a]
                #这里有一行需要：cdn判断，再加入data类对象record的cdn变量，record.cdn = cdn_address
                record.cdn = cdn_address
                #record['cdn'] = ips
        #print(record,self.records)

    def flow(self):                                     #流程控制方法
        #子域名扫描
        self.subdomain_brute()
        #CDN识别
        self.cdn_identify()

    #类方法，没有用到实例对象，可用用到类名cls代替，写入一下内容：代替用户创建实例化，以及流程，我们来告诉用户怎么用
    @classmethod                                    
    def start(cls):
        instance = cls("baidu.com")
        instance.flow()
        return instance
 



if __name__ == '__main__':
    scanner = Scanner.start()
    print(scanner)

