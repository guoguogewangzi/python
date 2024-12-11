#内置库
import webbrowser

#第三方库
from colorama import Fore,Style

#自定义库
from sherlock_project.result import QueryStatus

globvar = 0

class QueryNotify:

    # 构造方法
    def __init__(self, result=None):
        self.result = result

    def start(self, message=None):
        """"""

    def update(self, result):
        self.result = result


    def finish(self, message=None):
        """"""

    def __str__(self):
        return str(self.result)


class QueryNotifyPrint(QueryNotify):

    # 构造方法
    def __init__(self, result=None, verbose=False, print_all=False, browse=False):

        super().__init__(result)   #将 result 赋值到父类的 self.result 属性上。这样，self.result 成为了父类的属性，子类也可以访问它。
        self.verbose = verbose
        self.print_all = print_all
        self.browse = browse

        return

    #打印开始提示
    def start(self, message):

        title = "Checking username"

        #例如：[*] Checking username user on:
        print(Style.BRIGHT + Fore.GREEN + "[" +Fore.YELLOW + "*" +Fore.GREEN + f"] {title}" +Fore.WHITE + f" {message}" +Fore.GREEN + " on:")
        
        print('\r')

        return
    
    #用户存在结果计数，标记为Claimed（即用户名存在），则globvar加1
    def countResults(self):

        global globvar

        globvar += 1
        
        return globvar

    #
    def update(self, result):

        self.result = result

        response_time_text = ""

        #如果有响应时间并且verbose参数启用（即显示调试信息），则query_time预处理转存至response_time_text
        if self.result.query_time is not None and self.verbose is True:
            response_time_text = f" [{round(self.result.query_time * 1000)}ms]"

        #
        if result.status == QueryStatus.CLAIMED:
            self.countResults()
            
            #例如：[+]10.0 test: http://www.baidu.com
            print(Style.BRIGHT + Fore.WHITE + "[" +Fore.GREEN + "+" +Fore.WHITE + "]" +response_time_text +Fore.GREEN +f" {self.result.site_name}: " +Style.RESET_ALL +f"{self.result.site_url_user}")

            if self.browse:
                webbrowser.open(self.result.site_url_user, 2)

        elif result.status == QueryStatus.AVAILABLE:
            #参数print_all启用（即：打印找不到用户名的网站）
            if self.print_all:
                
                #例如：[-]10.0 test: Not Found!
                print(Style.BRIGHT + Fore.WHITE + "[" +Fore.RED + "-" +Fore.WHITE + "]" +response_time_text +Fore.GREEN + f" {self.result.site_name}:" +Fore.YELLOW + " Not Found!")

        elif result.status == QueryStatus.UNKNOWN:
            #参数print_all启用（即：打印找不到用户名的网站）
            if self.print_all:
                
                #例如：[-] test: context 
                print(Style.BRIGHT + Fore.WHITE + "[" +Fore.RED + "-" +Fore.WHITE + "]" +Fore.GREEN + f" {self.result.site_name}:" +Fore.RED + f" {self.result.context}" +Fore.YELLOW + " ")

        elif result.status == QueryStatus.ILLEGAL:
            #参数print_all启用（即：打印找不到用户名的网站）
            if self.print_all:
                msg = "Illegal Username Format For This Site!"
                
                #例如：[-] test: msg
                print(Style.BRIGHT + Fore.WHITE + "[" +Fore.RED + "-" +Fore.WHITE + "]" +Fore.GREEN + f" {self.result.site_name}:" +Fore.YELLOW + f" {msg}")
                
        elif result.status == QueryStatus.WAF:
            #参数print_all启用（即：打印找不到用户名的网站）
            if self.print_all:
                
                #例如：[-] test: Blocked by bot detection (proxy may help)
                print(Style.BRIGHT + Fore.WHITE + "[" +Fore.RED + "-" +Fore.WHITE + "]" +Fore.GREEN + f" {self.result.site_name}:" +Fore.RED + " Blocked by bot detection" +Fore.YELLOW + " (proxy may help)")

        else:
            raise ValueError(f"Unknown Query Status '{result.status}' for site '{self.result.site_name}'")

        return

    #打印结束语
    def finish(self, message="The processing has been finished."):

        NumberOfResults = self.countResults() - 1

        #例如：[*] Search completed with 31 results
        print(Style.BRIGHT + Fore.GREEN + "[" +Fore.YELLOW + "*" +Fore.GREEN + "] Search completed with" +Fore.WHITE + f" {NumberOfResults} " +Fore.GREEN + "results" + Style.RESET_ALL)

    
    #打印对象时调用该方法
    def __str__(self):
 
        return str(self.result)



