
#内置库
import json
import secrets

#第三方库
import requests

class SiteInformation:
    def __init__(self,name,url_home,url_username_format,username_claimed,information,is_nsfw,username_unclaimed=secrets.token_urlsafe(10)):
        self.name= name
        self.url_home = url_home
        self.url_username_format = url_username_format
        self.username_claimed = username_claimed
        self.information = information
        self.is_nsfw = is_nsfw

        return 

    def __str__(self):
        return f"{self.name}({self.url_home})"



class SitesInformation:
    def __init__(self,data_file_path=None):
        #{"网站名称":"对象（）"}
        self.sites = {}

        #加载data.json,site_data保存
        ##################################################################
        if not data_file_path: #没有路径
            data_file_path="https://raw.githubusercontent.com/sherlock-project/sherlock/master/sherlock_project/resources/data.json"
        if not data_file_path.lower().endswith(".json"):  #后缀不是.json
            raise FileNotFoundError(f"数据文件的JSON文件扩展名不正确 '{data_file_path}'. ")
        if data_file_path.lower().startswith("http"):  #如果通过在线获取的路径
            try:
                response = requests.get(url=data_file_path) #请求获取数据
            except Exception as error:
                raise FileNotFoundError(f"试图访问数据文件URL时出错 '{data_file_path}':  {error}")
            if response.status_code !=200:
                raise FileNotFoundError(f"响应不是200：'{data_file_path}'.")
            try:
                site_data = response.json() #>加载在线数据
            except Exception as error:
                raise ValueError(f"解析json内容时出错'{data_file_path}':{error}.")
        else:
            try:
                with open(data_file_path,'r',encoding="utf-8") as file:
                    try:
                        site_data = json.load(file) #>加载离线数据
                    except Exception as error:
                        raise ValueError(f"解析json内容出错{data_file_path}: {error}.")
            except FileNotFoundError:
                raise FileNotFoundError(f"数据文件json访问错误：{data_file_path}")
        
        site_data.pop("$schema",None)   #删除"$schema"键
        ##################################################################
        
        #site_data转存至self.sites,结构：{"网站名称":"对象（）"}
        #################################################################
        for site_name in site_data:
            try:

                self.sites[site_name] = SiteInformation(
                    site_name,                                 #网站名称
                    site_data[site_name]["urlMain"],           #网站主页（都有）
                    site_data[site_name]["url"],               #查询接口（都有）
                    site_data[site_name]["username_claimed"],  #示例用户名（都有）
                    site_data[site_name],                      #所有信息（字典类型）
                    site_data[site_name].get("isNSFW",False)   #是否存在isNFW键
                    )

            except KeyError as error:
                raise ValueError(f"解析json内容错误{data_file_path}:缺少属性{error}.")
            
            except TypeError:
                print(f"在解析JSON内容时遇到类型错误'{site_name}' at {data_file_path}跳过目标")
        #################################################################

        return 

    def remove_nsfw_sites(self, do_not_remove: list = []):
        sites = {}
        do_not_remove = [site.casefold() for site in do_not_remove]
        for site in self.sites:
            if self.sites[site].is_nsfw and site.casefold() not in do_not_remove:
                continue
            sites[site] =self.sites[site]
        
        self.sites = sites

    def site_name_list(self):
        return sorted([site.name for site in self],key = str.lower)
    
    def __iter__(self):
        for site_name in self.sites:
            yield self.sites[site_name]
    
    def __len__(self):
        return len(self.sites)
    





