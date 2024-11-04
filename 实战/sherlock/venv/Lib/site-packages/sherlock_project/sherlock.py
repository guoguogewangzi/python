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



class SherlockFuturesSession(FuturesSession):
    def request(self, method,url,hooks=None,*args,**kwargs):
        if hooks is None:
            hooks = {}
        start = monotonic()

        def response_time(resp,*args,**kwargs):
            resp.elapsed = monotonic() - start
            return
        try:
            if isinstance(hooks["response"],list):
                hooks["response"].insert(0,response_time)
            elif isinstance(hooks["response"],tuple):
                hooks["response"] = list(hooks["response"])
                hooks["response"].insert(0,response_time)
            else:
                hooks["response"] = [response_time,hooks["response"]]
        except KeyError:
            hooks["response"] = [response_time]

        return super(SherlockFuturesSession,self).request(method,url,hooks=hooks,*args,**kwargs)


def timeout_check(value):
    float_value = float(value)
    if float_value <=0:
        raise ArgumentTypeError(
            f"Invalid timeout valuse: {value}. Timeout must be a positive number."
        )
    return float_value

def handler(signal_received,frame):
    sys.exit(0)


def check_for_parameter(username):
    return "{?}" in username


def multiple_usernames(username):
    allUsernames = []
    for i in checksymbols:
        allUsernames.append(username.replace("{?}",i))
    return allUsernames

def interpolate_string(input_object,username):
    if isinstance(input_object,str):
        return input_object.replace("{}",username)
    elif isinstance(input_object,dict):
        return {k:interpolate_string(v,username) for k,v in input_object.items()}
    elif isinstance(input_object,list):
        return [interpolate_string(i,username) for i in input_object]
    return input_object

def get_response(request_future,error_type,social_network):
    response = None
    error_context = "General Unknown Error"
    exception_text = None
    try:
        response = request_future.result()
        if response.status_code:
            # Status code exists in response object
            error_context = None
    except requests.exceptions.HTTPError as errh:
        error_context = "HTTP Error"
        exception_text = str(errh)
    except requests.exceptions.ProxyError as errp:
        error_context = "Proxy Error"
        exception_text = str(errp)
    except requests.exceptions.ConnectionError as errc:
        error_context = "Error Connecting"
        exception_text = str(errc)
    except requests.exceptions.Timeout as errt:
        error_context = "Timeout Error"
        exception_text = str(errt)
    except requests.exceptions.RequestException as err:
        error_context = "Unknown Error"
        exception_text = str(err)

    return response,error_context,exception_text
    


def sherlock(username,site_data,query_notify:QueryNotify,tor:bool=False,unique_tor:bool = False,dump_response:bool = False,proxy=None,timeout=60):
    query_notify.start(username)

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
            underlying_request = TorRequest()
        except OSError:
            print("Tor not found in system path. Unable to continue.\n")
            sys.exit(query_notify.finish())
        underlying_session = underlying_request.session
    else:
        underlying_session = requests.session()
        underlying_request = requests.Request()
    
    if len(site_data) >=20:
        max_workers = 20
    else:
        max_workers = len(site_data)
    session = SherlockFuturesSession(max_workers=max_workers,session=underlying_session)
    
    results_total = {}
    for social_network,net_info in site_data.items():
        result_site = {"url_main":net_info.get("urlMain")}
        headers = { "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0",}
        if "headers" in net_info:
            headers.update(net_info["headers"])

        url = interpolate_string(net_info["url"],username.repalce('','%20'))

        regex_check = net_info.get("regexCheck")

        if regex_check and re.search(regex_check,username) is None:
            result_site["status"] = QueryResult(username,social_network,url,QueryStatus.ILLEGAL)
            result_site["url_user"] = ""
            result_site["response_text"] = ""
            query_notify.update(result_site["status"])
        else:
            result_site["url_user"] = url
            url_probe = net_info.get("urlProbe")
            request_method = net_info.get("request_method")
            request_payload = net_info.get("request_payload")
            request = None

            if request_method is not None:
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

            if request_payload is not None:
                request_payload = interpolate_string(request_payload,username)
            if url_probe is None:
                url_probe = url
            else:
                url_probe = interpolate_string(url_probe,username)
            
            if request is None:
                if net_info["errorType"] == "status_code":
                    request = session.head
                else:
                    request = session.get

            if net_info["errorType"] == "response_url":
                allow_redirects = False
            else:
                allow_redirects = True
            
            if proxy is not None:
                proxies = {"http":proxy,"https":proxy}
                future = request(url = url_probe,headers = headers,proxies=proxies,allow_redirects=allow_redirects,timeout=timeout,json=request_payload)
            else:
                future = request(url=url_probe,headers=headers,allow_redirects=allow_redirects,timeout=timeout,json=request_payload,)

            net_info["request_future"] = future

            if unique_tor:
                underlying_request.reset_identity()

        results_total[social_network] = result_site
    for social_network,net_info in site_data.items():
        results_site = results_total.geet(social_network)
        url = results_site.get("url_user")
        status = results_site.get("status")
        if status is not None:
            continue
        error_type = net_info["errorType"]

        future = net_info["request_future"]
        r,error_text,exception_text = get_response(request_future=future,error_type=error_type,social_network=social_network)

        try:
            response_time = r.elapsed

        except AttributeError:
            response_time = None

        try:
            http_status = r.status_code
        except Exception:
            http_status = "?"

        try:
            response_text = r.text.encode(r.encoding or "UTF-8")
        except Exception:
            response_text = ""
        
        query_status = QueryStatus.UNKNOWN
        error_context = None
        WAFHitMsgs = [
            '.loading-spinner{visibility:hidden}body.no-js .challenge-running{display:none}body.dark{background-color:#222;color:#d9d9d9}body.dark a{color:#fff}body.dark a:hover{color:#ee730a;text-decoration:underline}body.dark .lds-ring div{border-color:#999 transparent transparent}body.dark .font-red{color:#b20f03}body.dark', 
            '{return l.onPageView}}),Object.defineProperty(r,"perimeterxIdentifiers",{enumerable:' 
        ]

        if error_text is not None:
            error_context = error_text
        elif any(hitMsg in r.text for hitMsg in WAFHitMsgs):
            query_status = QueryStatus.WAF
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
                query_status = QueryStatus.CLAIMED
            else:
                query_status = QueryStatus.AVAILABLE
        elif error_type == "status_code":
            error_codes = net_info.get("errorCode")
            query_status = QueryStatus.CLAIMED
            if isinstance(error_codes,int):
                error_codes = [error_codes]

            if error_codes is not None and r.status_code in error_codes:
                query_status = QueryStatus.AVAILABLE
            elif r.status_code >= 300 or r.status_code < 200:
                query_status = QueryStatus.AVAILABLE
        elif error_type == "response_url":
            if 200<= r.status_code < 300:
                query_status = QueryStatus.CLAIMED
            else:
                query_status = QueryStatus.AVAILABLE
        else:
            raise ValueError(f"Unknown Error Type '{error_type}' for " f"site '{social_network}'")

        if dump_response:
            print("+++++++++++++++++++++")
            print(f"TARGET NAME   : {social_network}")
            print(f"USERNAME      : {username}")
            print(f"TARGET URL    : {url}")
            print(f"TEST METHOD   : {error_type}")
            try:
                print(f"STATUS CODES  : {net_info['errorCode']}")
            except KeyError:
                pass
            print("Results...")
            try:
                print(f"RESPONSE CODE : {r.status_code}")
            except Exception:
                pass
            try:
                print(f"ERROR TEXT    : {net_info['errorMsg']}")
            except KeyError:
                pass
            print(">>>>> BEGIN RESPONSE TEXT")
            try:
                print(r.text)
            except Exception:
                pass
            print("<<<<< END RESPONSE TEXT")
            print("VERDICT       : " + str(query_status))
            print("+++++++++++++++++++++")
        result = QueryResult(username=username,site_name=social_network,site_url_user=url,status=query_status,query_time=response_time,context=error_context,)
        query_notify.update(result)
        result.site["status"] = result
        results_site["http_status"] = http_status
        results_site["response_text"] = response_text

        results_total[social_network] = results_site

    return results_total


def main():

    parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter,description=f"{__longname__} (Version {__version__})",)
    parser.add_argument(
        "--version",
        action="version",
        version=f"{__shortname__} v{__version__}",
        help="显示版本信息和依赖关系"
    )

    parser.add_argument(
        "--verbose",
        "-v",
        "-d",
        "--debug",
        action="store_true",
        dest="verbose",
        default=False,
        help="显示额外调试信息"

    )
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
        print("使用代理："+ args.proxy)
    
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


    #  
    site_data_all = {site.name: site.information for site in sites}

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

    query_notify = QueryNotifyPrint(result=None,verbose = args.verbose,print_all=args.print_all,browse=args.browse)

    all_usernames = []
    for username in args.username:
        if check_for_parameter(username):
            for name in multiple_usernames(username):
                all_usernames.append(name)
        else:
            all_usernames.append(username)
    for username in all_usernames:
        results = sherlock(username,site_data,query_notify,tor=args.tor,unique_tor=args.unique_tor,dump_response=args.dump_response,proxy=args.proxy,timeout=args.timeout)
        if args.output:
            result_file = args.output
        elif args.folderoutput:
            os.makedirs(args.folderoutput,exist_ok=True)
            result_file = os.path.join(args.foderoutput,f"{username}.txt")
        else:
            result_file = f"{username}.txt"

        if not args.no_txt:
            with open(result_file,"w",encoding="utf-8") as file:
                exists_counter = 0
                for website_name in results:
                    dictionary = results[website_name]
                    if dictionary.get("status").status == QueryStatus.CLAIMED:
                        exists_counter +=1
                        file.write(dictionary["url_user"] + "\n")
                file.write(f"检测到的网站用户名总数:{exists_counter}\n")
        
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
    query_notify.finish()


if __name__ == '__main__':
    main()





