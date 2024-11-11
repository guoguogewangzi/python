#内置库
import sys,os,csv,re
from argparse import ArgumentParser,RawDescriptionHelpFormatter,ArgumentTypeError
import signal
from json import loads as json_loads
from time import monotonic

#第三方库
import requests
from colorama import init
import pandas as pd
from requests_futures.sessions import FuturesSession

#自定义库
from sherlock_project.__init__ import(__longname__,__shortname__,__version__,forge_api_latest_release,)
from sherlock_project.sites import SitesInformation
from sherlock_project.notify import QueryNotify
from sherlock_project.notify import QueryNotifyPrint
from sherlock_project.result import QueryStatus
from sherlock_project.result import QueryResult
try:
    from sherlock_project.__init__ import import_error_test_var
except ImportError:
    print("是否使用了 python3 sherlock/sherlock.py ... 这种运行方式")
    print("这是一个过时的启动方式，请参考：https://sherlockproject.xyz/installation，获取最新说明")
    sys.exit(1)


checksymbols = ["_", "-", "."]


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


def timeout_check(value):
    float_value = float(value)
    if float_value <=0:
        raise ArgumentTypeError(
            f"Invalid timeout valuse: {value}. Timeout must be a positive number."
        )
    return float_value

def handler(signal_received,frame):
    sys.exit(0)

#判断用户名是否存在 {?} 符号，返回True或False
def check_for_parameter(username):
    return "{?}" in username

#输入"test{?}t"，返回：['test_t', 'test-t', 'test.t']
#########################################################
def multiple_usernames(username):
    allUsernames = []
    for i in checksymbols:
        allUsernames.append(username.replace("{?}",i))
    return allUsernames
#########################################################

#查询接口url处理，将{}替换为username
#####################################################
def interpolate_string(input_object,username):
    if isinstance(input_object,str):          #input_object，如果是字符串
        return input_object.replace("{}",username)
    
    elif isinstance(input_object,dict):       #input_object，如果是字典
        return {k:interpolate_string(v,username) for k,v in input_object.items()}
    
    elif isinstance(input_object,list):       #input_object，如果是列表
        return [interpolate_string(i,username) for i in input_object]
    
    return input_object
#####################################################

#返回请求响应的结果，以及错误信息类型，和详细错误信息
###############################################################
def get_response(request_future,error_type,social_network):
    response = None
    error_context = "General Unknown Error"  #用于存储错误的上下文信息，默认为：“General Unknown Error”，意味着如果发生错误，但没有特别的处理，最终会返回此错误信息。
    exception_text = None  # 用于存储异常的详细信息
    try:
        response = request_future.result()   #获取请求响应的结果

        if response.status_code:     #如果响应的status_code 存在且有效，error_context会被设置为None,表示没有发生错误。

            # Status code exists in response object
            error_context = None
    
    #请求的返回错误状态码，如404或500时会抛出此异常，异常信息会被存储到exception_text中，并且错误上下文被设置为：“HTTP Error”
    except requests.exceptions.HTTPError as errh:
        error_context = "HTTP Error"
        exception_text = str(errh)
    
    #如果请求过程中发生代理错误，则捕获此异常
    except requests.exceptions.ProxyError as errp:
        error_context = "Proxy Error"
        exception_text = str(errp)
    
    #如果发生网络连接问题，则捕获此异常
    except requests.exceptions.ConnectionError as errc:
        error_context = "Error Connecting"
        exception_text = str(errc)

    #如果请求因超时而失败，将触发此异常
    except requests.exceptions.Timeout as errt:
        error_context = "Timeout Error"
        exception_text = str(errt)

    #requests库的基类异常，捕获所有未被具体分类的请求异常
    except requests.exceptions.RequestException as err:
        error_context = "Unknown Error"
        exception_text = str(err)

    #最终返回三个值：1.请求响应的结果，2.错误类型描述，请求成功则为None,如果发生错误则包含对应的错误上下文（如HTTP Error，Proxy Error等），3.错误的详细信息
    return response,error_context,exception_text
###############################################################


def sherlock(username,site_data,query_notify:QueryNotify,tor:bool=False,unique_tor:bool = False,dump_response:bool = False,proxy=None,timeout=60):
    
    #打印开始提示：“[*] Checking username test1 test2 on:”
    query_notify.start(username)

    #判断tor或unique_tor是否存在，以及实例化HTTP请求模块
    #############################################################################################
    if tor or unique_tor:
        try:
            from torrequest import TorRequest
        except ImportError:
            print("Important!")
            print("> --tor and --unique-tor are now DEPRECATED, and may be removed in a future release of Sherlock.")
            print("> If you've installed Sherlock via pip, you can include the optional dependency via `pip install 'sherlock-project[tor]'`.")
            print("> Other packages should refer to their documentation, or install it separately with `pip install torrequest`.\n")
            sys.exit(query_notify.finish())
        print("Important!")
        print("> --tor and --unique-tor are now DEPRECATED, and may be removed in a future release of Sherlock.")
    
        try:
            underlying_request = TorRequest()    #如果存在，则使用TorRequest()实例化
        except OSError:
            print("Tor not found in system path. Unable to continue.\n")
            sys.exit(query_notify.finish())
        underlying_session = underlying_request.session
    else:
        underlying_session = requests.session() #如果不存在，则使用requests.session()实例化
        underlying_request = requests.Request() #如果不存在，则使用requests.Request()实例化
    #################################################################################################

    #最大并发参数设置：20
    ##########################
    if len(site_data) >=20:
        max_workers = 100
    else:
        max_workers = len(site_data)
    ##########################

    #实例化网络并发实例
    session = SherlockFuturesSession(max_workers=max_workers,session=underlying_session)
    

    results_total = {}
    for social_network,net_info in site_data.items():

        results_site = {"url_main":net_info.get("urlMain")} #赋值，urlMain键和值

        headers = { "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0",} 
        
        if "headers" in net_info:                #如果库存在headers字段
            headers.update(net_info["headers"])  #则更新headers

        url = interpolate_string(net_info["url"],username.replace(' ','%20'))   #查询接口拼接用户名

        regex_check = net_info.get("regexCheck") #获取regexCheck的值

        if regex_check and re.search(regex_check,username) is None:              #如果存在正则表达式，并且username不匹配正则表达式，是空的
            results_site["status"] = QueryResult(username, social_network, url, QueryStatus.ILLEGAL)#存储状态,状态：1.用户名，2.网站名，3.查询的url，4.标记：为用户名不合法
            results_site["url_user"] = ""                          
            results_site["http_status"] = ""
            results_site["response_text"] = ""
            query_notify.update(results_site["status"])
        else:                                                    #否则，用户名合法
            results_site["url_user"] = url                        #记录:查询的url
            url_probe = net_info.get("urlProbe")                 #记录（如果存在,否则None）：真正的API URL
            request_method = net_info.get("request_method")      #记录（如果存在,否则None）：请求方法
            request_payload = net_info.get("request_payload")    #记录（如果存在,否则None）：请求payload
            request = None

            #定义请求方法
            #############################################
            if request_method is not None:                       #如果请求方法不是空（自添加）
                if request_method == "GET":
                    request = session.get
                elif request_method == "HEAD":
                    request = session.head
                elif request_method == "POST":
                    request = session.post
                elif request_method == "PUT":
                    request = session.put
                else:
                    raise RuntimeError(f"Unsupported request_method for {url}")
            #############################################

            #待替换的{}，{}在request_payload情况处理
            if request_payload is not None:
                request_payload = interpolate_string(request_payload,username)

            #真正的查询接口不存在
            if url_probe is None:
                url_probe = url

            #真正的查询接口存在
            else:                 
                url_probe = interpolate_string(url_probe,username)
            
            #未自添加请求方法
            if request is None:
                #默认为head方法
                if net_info["errorType"] == "status_code":  #如果为status_code类型,tip:"errorType"有三种类型："message"，"status_code"，"response_url"
                    request = session.head
                #如果未添加"errorType"，则为get请求方法
                else:
                    request = session.get
            
            #如果为：response_url类型，则不允许重定向
            if net_info["errorType"] == "response_url":
                allow_redirects = False
            else:
                allow_redirects = True
            
            #如果没有设置代理
            if proxy is not None:
                proxies = {"http":proxy,"https":proxy}

                future = request(url = url_probe,headers = headers,proxies=proxies,allow_redirects=allow_redirects,timeout=timeout,json=request_payload)  #发起请求

            else:
                future = request(url=url_probe,headers=headers,allow_redirects=allow_redirects,timeout=timeout,json=request_payload,) #发起请求

            #存储请求结果
            net_info["request_future"] = future


            if unique_tor:
                underlying_request.reset_identity()     #确保接下来的请求不携带以前的身份数据

        results_total[social_network] = results_site    #转存results_site至results_total

    

    for social_network,net_info in site_data.items():  #遍历data.json里的数据
        
        results_site = results_total.get(social_network) #从处理后的results_total里获取对应的站点信息

        url = results_site.get("url_user")     #获取待查询的url

        status = results_site.get("status")    #获取存储的状态，包括：1.用户名，2.网站名，3.查询的url，4.标记：为用户名不合法
        
        #如果获取的状态不是空的（即用户名不合法），即结束，跳出循环，否则继续其他处理
        if status is not None:
            continue

        error_type = net_info["errorType"]   #获取errorType类型

        future = net_info["request_future"]  #获取存储的请求结果

        # 返回请求响应的结果，以及错误信息类型，和详细错误信息
        r,error_text,exception_text = get_response(request_future=future,error_type=error_type,social_network=social_network)

        #获取请求的响应时间
        #######################################
        try:
            response_time = r.elapsed    

        except AttributeError:
            response_time = None
        #######################################

        #获取响应状态码
        #######################################
        try:
            http_status = r.status_code
        except Exception:
            http_status = "?"
        #######################################

        #获取响应内容
        #######################################
        try:
            response_text = r.text.encode(r.encoding or "UTF-8")
        except Exception:
            response_text = ""
        #######################################

        #首先标记“用户名未知”
        query_status = QueryStatus.UNKNOWN

        #设置错误类型为None
        error_context = None

        #用于匹配被WAF拦截时返回的响应特征
        WAFHitMsgs = [
            '.loading-spinner{visibility:hidden}body.no-js .challenge-running{display:none}body.dark{background-color:#222;color:#d9d9d9}body.dark a{color:#fff}body.dark a:hover{color:#ee730a;text-decoration:underline}body.dark .lds-ring div{border-color:#999 transparent transparent}body.dark .font-red{color:#b20f03}body.dark', 
            '{return l.onPageView}}),Object.defineProperty(r,"perimeterxIdentifiers",{enumerable:' 
        ]

        #如果返回的错误类型不空，则转存至error_context
        if error_text is not None:
            error_context = error_text

        #如果是waf的返回信息，则标记为waf
        elif any(hitMsg in r.text for hitMsg in WAFHitMsgs):
            query_status = QueryStatus.WAF
        
        #情况1：message，默认存在该用户名（即error_flag =True），只要存在了指定的错误信息，则不存在该用户名（即error_flag =False）
        ##########################################
        elif error_type == "message":
            error_flag =True
            errors = net_info.get("errorMsg")
            if isinstance(errors,str):
                if errors in r.text:
                    error_flag = False
            else:
                for error in errors:
                    if error in r.text:
                        error_flag =False
                        break
            if error_flag:
                query_status = QueryStatus.CLAIMED       #存在标记
            else:
                query_status = QueryStatus.AVAILABLE     #不存在标记
        ##########################################

        #情况2：status_code，默认存在，如果在指定的状态码里面，或者返回的状态码大于等于300，或者小于200，则不存在
        ##########################################
        elif error_type == "status_code":
            error_codes = net_info.get("errorCode")
            query_status = QueryStatus.CLAIMED         #默认存在标记
            if isinstance(error_codes,int):
                error_codes = [error_codes]

            if error_codes is not None and r.status_code in error_codes:     #如果：返回的状态码在指定的状态码里面，则不存在
                query_status = QueryStatus.AVAILABLE                         #不存在标记

            elif r.status_code >= 300 or r.status_code < 200:                #如果：返回的状态码大于等于300，或者小于200，则不存在
                query_status = QueryStatus.AVAILABLE                         #不存在标记
        ##########################################


        #情况3：response_url，果返回的状态码大于等于200，并且小于300，则存在
        ##########################################
        elif error_type == "response_url":              
            if 200<= r.status_code < 300:                 #如果返回的状态码大于等于200，并且小于300，则存在
                query_status = QueryStatus.CLAIMED         #存在标记
            else:
                query_status = QueryStatus.AVAILABLE        #不存在标记
        ##########################################
        
        #否则报未知的error_type类型错误
        else:
            raise ValueError(f"Unknown Error Type '{error_type}' for " f"site '{social_network}'")

        #打印三类信息：data.json部分信息，响应的状态码和文本，判断结果
        ############################################################
        if dump_response:
            print("+++++++++++++++++++++")
            print(f"TARGET NAME   : {social_network}")        #打印网站名称
            print(f"USERNAME      : {username}")              #打印用户名
            print(f"TARGET URL    : {url}")                   #打印待查询的url
            print(f"TEST METHOD   : {error_type}")            #打印判断类型（反向判断），error_type
            try:
                print(f"STATUS CODES  : {net_info['errorCode']}") #如果有errorCode（data.json中），则打印
            except KeyError:
                pass

            print("Results...")

            try:
                print(f"RESPONSE CODE : {r.status_code}")    #打印返回的状态码
            except Exception:
                pass
            try:
                print(f"ERROR TEXT    : {net_info['errorMsg']}")   #如果有errorMsg（data.json中），则打印
            except KeyError:
                pass

            print(">>>>> BEGIN RESPONSE TEXT")
            try:
                print(r.text)                               #打印响应文本
            except Exception:
                pass
            print("<<<<< END RESPONSE TEXT")
            print("VERDICT       : " + str(query_status))   #打印判断结果
            print("+++++++++++++++++++++")
        ############################################################

        #将结果转存至实例化result中
        result = QueryResult(username=username,site_name=social_network,site_url_user=url,status=query_status,query_time=response_time,context=error_context,)


        query_notify.update(result)                            #更新result

        results_site["status"] = result                        #result保存至results_site中
        results_site["http_status"] = http_status              #同时保存http_status（返回状态码）
        results_site["response_text"] = response_text          #同时保存response_text（返回文本）

        results_total[social_network] = results_site           #results_site转存至results_total

    return results_total                                       #返回results_total


def main():

    parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter,description=f"{__longname__} (Version {__version__})",)

    parser.add_argument("--version",action="version",version=f"{__shortname__} v{__version__}",help="显示版本信息和依赖关系")
    parser.add_argument("--verbose","-v","-d","--debug",action="store_true",dest="verbose",default=False,help="显示额外调试信息")
    parser.add_argument("--folderoutput","-fo",dest="folderoutput",help="如果是多个用户名，输出结果将保存至该文件夹")
    parser.add_argument("--output","-o",dest="output",help="如果是单个用户名，输出结果将保存至该文件夹")
    parser.add_argument("--tor","-t",action="store_true",dest="tor",default=False,help="通过tor发送请求，需要安装Tor并已添加系统路径")
    parser.add_argument("--unique-tor","-u",action="store_true",dest="unique_tor",default=False,help="每次Tor请求后，通过新的Tor电路发出请求，需要安装Tor并已添加系统路径")
    parser.add_argument("--csv",action="store_true",dest="csv",default=False,help="创建CSV文件")
    parser.add_argument("--xlsx",action="store_true",dest="xlsx",default=False,help="创建xlsx文件")
    parser.add_argument("--site",action="append",metavar="SITE_NAME",dest="site_list",default=[],help="添加指定站点")
    parser.add_argument("--proxy","-p",metavar="PROXY_URL",action="store",dest="proxy",default=None,help="代理，比如：socks5://127.0.0.1:1080")
    parser.add_argument("--dump-response",action="store_true",dest="dump_response",default=False,help="将HTTP响应转至标准输出针对性调试")
    parser.add_argument("--json","-j",metavar="JSON_FILE",dest="json_file",default=None,help="从json文件或在线有效json文件加载数据")
    parser.add_argument("--timeout",action="store",metavar="TIMEOUT",dest="timeout",type=timeout_check,default=60,help="等待请求响应时间（以秒为单位）默认值：60")
    parser.add_argument("--print-all",action="store_true",dest="print_all",default=False,help="打印找不到用户名的网站")
    parser.add_argument("--print-found",action="store_true",dest="print_found",default=True,help="打印找到用户名的网站")
    parser.add_argument("--no-color",action="store_true",dest="no_color",default=False,help="终端输出不带颜色")
    parser.add_argument("username",nargs="+",metavar="USERNAMES",action="store",help="用于检查社交网络的一个或多个用户名。使用 {?} 检查相似的用户名（替换为“_”、“-”、“.”）。")
    parser.add_argument("--browse","-b",action="store_true",dest="browse",default=False,help="在默认浏览器浏览所有结果")
    parser.add_argument("--local","-l",action="store_true",default=False,help="强制使用本地的data.json文件")
    parser.add_argument("--nsfw",action="store_true",default=False,help="从默认列表中检查NSFW")
    parser.add_argument("--no-txt",action="store_true",dest="no_txt",default=False,help="禁用创建txt文件")

    args = parser.parse_args()

    signal.signal(signal.SIGINT,handler)

    #检查是否有新的Sherlock版本。如果有，则通知
    try:
        latest_release_raw = requests.get(forge_api_latest_release).text
        latest_release_json = json_loads(latest_release_raw)
        latest_remote_tag = latest_release_json["tag_name"]

        if latest_remote_tag[1:] != __version__:
            print(
                f"Update available！{__version__} --> {latest_remote_tag[1:]}"
                f"\n{latest_release_json['html_url']}"

            )

    except Exception as error:
        print(f"检查更新时出现错误：{error}")

    #是否同时使用Tor和proxy参数
    if args.tor and (args.proxy is not None):
        raise Exception("Tor 和 Proxy 不能同时设置")

    #proxy是否不是空
    if args.proxy is not None:
        print("Using the proxy:"+ args.proxy)
    
    #tor或unique_tor参数是否存在
    if args.tor or args.unique_tor:
        print("使用Tor发送请求")

        print("警告：一些网站可能会拒绝通过Tor连接,所以请注意使用此选项可能会增加连接错误")

    #终端颜色参数是否存在
    if args.no_color:
        init(strip=True,convert=False)
    else:
        init(autoreset=True)

    #output和folderoutput是否都不是空
    if args.output is not None and args.folderoutput is not None:
        print("您只能使用其中一种输出方法")
        sys.exit(1)

    #output是否不是空，以及username长度不等于1
    if args.output is not None and len(args.username) !=1:
        print("--output参数需与单个用户名一起使用")
        sys.exit(1)
    

    #是否使用离线网站库
    try:
        if args.local:
            sites = SitesInformation(os.path.join(os.path.dirname(__file__), "resources/data.json"))
        else:
            sites = SitesInformation(args.json_file)
    except Exception as error:
        print(f"ERROR:  {error}")
        sys.exit(1)


    #如果没有nsfw（不适合在工作场合访问的内容），则移除nsfw列表，同时会保留指定的站点列表
    if not args.nsfw:
        sites.remove_nsfw_sites(do_not_remove=args.site_list)


    #sites对象里的数据 转存 site_data_all字典
    site_data_all = {site.name: site.information for site in sites}

    #site_data_all 处理至 site_data
    #############################################################################
    #如果指定的站点列表为空
    if args.site_list == []:
        site_data = site_data_all
    else:
        site_data={}
        site_missing = {}
        for site in args.site_list:
            counter = 0
            for existing_site in site_data_all:
                if site.lower() == existing_site.lower():   #如果指定的站点在网站库里，忽略大小写，字典的键比较
                    site_data[existing_site] = site_data_all[existing_site] #*如果找到匹配的站点，将其加入 site_data 中
                    counter +=1
            if counter ==0:
                site_missing.append(f"'{site}'") #如果在 site_data_all 中找不到指定的站点（counter == 0），则将其记录在 site_missing 列表中,以便后续提醒用户

            if site_missing:
                print(f"错误：未找到所需站点：{', '.join(site_missing)}.")
            if not site_data:
                sys.exit(1)
    #############################################################################

    #verbose:显示额外调试信息,print_all:打印找不到用户名的网站,browse:在默认浏览器浏览所有结果
    query_notify = QueryNotifyPrint(result=None,verbose = args.verbose,print_all=args.print_all,browse=args.browse)

    #用户名转存至all_usernames
    #################################################
    all_usernames = []
    for username in args.username:
        if check_for_parameter(username):
            for name in multiple_usernames(username):
                all_usernames.append(name)
        else:
            all_usernames.append(username)
    #################################################


    for username in all_usernames:
        
        #传参：username(处理后)，site_data(处理后),query_notify,tor,unique_tor,dump_response,proxy,timeout，返回结果
        results = sherlock(username,site_data,query_notify,tor=args.tor,unique_tor=args.unique_tor,dump_response=args.dump_response,proxy=args.proxy,timeout=args.timeout)

        #待保存的文件
        ###################################
        if args.output:
            result_file = args.output

        elif args.folderoutput:
            
            os.makedirs(args.folderoutput,exist_ok=True)
            
            result_file = os.path.join(args.foderoutput,f"{username}.txt")

        else:
            result_file = f"{username}.txt"
        ###################################

        #如果没有指定args.no_txt，写入txt文件
        if not args.no_txt:
            with open(result_file,"w",encoding="utf-8") as file:
                exists_counter = 0
                for website_name in results:
                    dictionary = results[website_name]
                    if dictionary.get("status").status == QueryStatus.CLAIMED:   #判断是否是存在标识
                        exists_counter +=1
                        file.write(dictionary["url_user"] + "\n")                #写入带用户名的url
                file.write(f"检测到的网站用户名总数:{exists_counter}\n")           
        
        #如果指定csv参数,写入csv文件
        if args.csv:
            result_file = f"{username}.csv"
            if args.folderoutput:
                os.makedirs(args.foderoutput,exist_ok=True)
                result_file = os.path.join(args.folderoutput,result_file)
            
            with open(result_file,"w",newline="",encoding="utf-8") as csv_report:
                writer = csv.writer(csv_report)
                writer.writerow(["username","name","url_main","url_user","exists","http_status","response_time_s"])
                for site in results:
                    if(args.print_found and not args.print_all and results[site]["status"].status !=QueryStatus.CLAIMED):
                        continue
                    response_time_s = results[site]["status"].query_time
                    if response_time_s is None:
                        response_time_s = ""
                    writer.writerow([username,site,results[site]["url_main"],results[site]["url_user"],str(results[site]["status"].status),results[site]["http_status"],response_time_s,])
        
        #如果指定xlsx参数，写入xlsx文件
        if args.xlsx:
            usernames=[]
            names = []
            url_main = []
            url_user = []
            exists = []
            http_status = []
            response_time_s = []
            
            for site in results:
                if (args.print_found and not args.print_all and results[site]["status"].status != QueryStatus.CLAIMED):
                    continue

                if response_time_s is None:
                    response_time_s.append("")
                else:
                    response_time_s.append(results[site]["status"].query_time)
                usernames.append(username)
                names.append(site)
                url_main.append(results[site]["url_main"])
                url_user.append(results[site]["url_user"])
                exists.append(str(results[site]["status"].status))
                http_status.append(results[site]["http_status"])
            
            DataFrame = pd.DataFrame({"username":usernames,"name":names,"url_main":url_main,"url_user":url_user,"exists":exists,"http_status":http_status,"response_time_s":response_time_s,})
            DataFrame.to_excel(f"{username}.xlsx",sheet_name="sheet1",index=False)
        
        print()
    
    #结束语：[*] Search completed with 20 results
    query_notify.finish()


if __name__ == '__main__':
    main()





