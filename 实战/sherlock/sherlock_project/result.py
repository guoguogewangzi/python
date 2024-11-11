from enum import Enum

class QueryStatus(Enum):
    CLAIMED   = "Claimed"   #用户名存在标识
    ILLEGAL   = "Illegal"   #用户名不允许在此网站使用
    AVAILABLE = "Available" #用户名未检测到
    UNKNOWN   = "Unknown"   #用户名未知
    WAF       = "WAF"       #请求被waf阻止

    def __str__(self):
        return self.value


class QueryResult:
    def __init__(self,username,site_name,site_url_user,status,query_time=None,context=None):
        self.username = username
        self.site_name = site_name
        self.site_url_user = site_url_user
        self.status = status
        self.query_time = query_time
        self.context = context

        return

    def __str__(self):
        status = str(self.status)
        if self.context is not None:
            status += f"({self.context})"
        return status

