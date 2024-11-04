
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
        if not data_file_path:
            data_file_path="https://raw.githubusercontent.com/sherlock-project/sherlock/master/sherlock_project/resources/data.json"
        if not data_file_path.lower().endswith(".json"):
            raise FileNotFoundError(f"数据文件的JSON文件扩展名不正确 '{data_file_path}'. ")
        if data_file_path.lower().startswith("http"):
            try:
                response = requests.get(url=data_file_path)
            except Exception as error:
                raise FileNotFoundError(f"试图访问数据文件URL时出错 '{data_file_path}':  {error}")
            if response.status_code !=200:
                raise FileNotFoundError(f"响应不是200：'{data_file_path}'.")
            try:
                site_data = response.json()
            except Exception as error:
                raise ValueError(f"解析json内容时出错'{data_file_path}':{error}.")
        else:
            try:
                with open(data_file_path,'r',encoding="utf-8") as file:
                    try:
                        site_data = json.load(file)
                    except Exception as error:
                        raise ValueError(f"解析json内容出错{data_file_path}: {error}.")
            except FileNotFoundError:
                raise FileNotFoundError(f"数据文件json访问错误：{data_file_path}")
        
        site_data.pop("$schema",None)

        self.sites = {}

        for site_name in site_data:
            try:
                self.sites[site_name] = SiteInformation(site_name,site_data[site_name]["urlMain"],site_data[site_name]["url"],site_data[site_name]["username_claimed"],site_data[site_name],site_data[site_name].get("isNSFW",False))
            except KeyError as error:
                raise ValueError(f"解析json内容错误{data_file_path}:缺少属性{error}.")
            except TypeError:
                print(f"在解析JSON内容时遇到类型错误'{site_name}' at {data_file_path}跳过目标")

        return 

    def remove_nsfw_sites(self, do_not_remove: list = []):
        sites = {}
        do_not_remove = [site.casefold() for site in do_not_remove]
        for site in self.sites:
            if self.sites[site].is_nsfw and site.casefold() not in do_not_remove:
                continue
            site[site] =self.sites[site]
        
        self.sites = sites

    def site_name_list(self):
        return sorted([site.name for site in self],key = str.lower)
    
    def __iter__(self):
        for site_name in self.sites:
            yield self.sites[site_name]
    
    def __len__(self):
        return len(self.sites)
    





