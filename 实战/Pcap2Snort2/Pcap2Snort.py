#-*- coding: utf-8 -*-

#内置库
import argparse,os,sys,json,time,hashlib

#第三方库
try:
    import dpkt
except Exception as e:
    raise e

pcap_ext = [".pcap"]


#命令行参数解析
##############################################################################################################
def cmdlineparser():
    parser = argparse.ArgumentParser(
        description="Powered by test", usage="python3 Pcap2Snort.py -p ./pcap", add_help=True)
    parser.add_argument(
        "-p", "--pcap", help="输入待提取snort规则的pcap目录或者文件绝对路径,eg.E:\\PcapTest or E:\\PcapTest\\test.pcap")

    args, unknown = parser.parse_known_args()

    #首先判断是否存在args.pcap参数，不存在则打印帮助信息，其次判断其路径是否存在，不存在则打印帮助信息
    ######################################################
    if not args.pcap or not os.path.exists(args.pcap):
        parser.print_help()
        sys.exit()
    ######################################################

    return args
##############################################################################################################

#“任务：分析Pcap，输出snort规则”类
#一级###########################################################################################################################################


class Pcap2Snort(object):
    def __init__(self) -> None:
        self.policy = dict()  #实例属性："规则策略"字典
        self.curdir = os.path.dirname(
            os.path.realpath(__file__))  #实例属性："py文件所在的文件夹路径"字符串
        self.policy_path = os.path.join(
            self.curdir, "Pcap2Snort.json")  #实例属性："策略文件路径"字符串
        self.snortlib = os.path.join(
            self.curdir, "snortlib")  #实例属性："snort规则存储库路径"字符串

        #如果"snort规则存储库路径"字符串不存在，则创建
        #三级#####################################
        if not os.path.exists(self.snortlib):
            os.mkdir(self.snortlib)
        #三级#####################################

    #从self.policy_path，读取实例的json策略文件，赋值策略变量:self.policy
    #二级####################################################
    def load_policy(self):
        try:
            with open(self.policy_path, "rb") as fr:
                self.policy = json.load(fr)
        except Exception as e:
            raise e
    #二级####################################################

    #输入pcap文件夹或pcap文件路径，逐个返回pcap文件路径
    #二级############################################################
    def load_pcap(self, pcappath: str) -> iter:

        if os.path.isdir(pcappath):
            for root, dirname, filenames in os.walk(pcappath):
                for filename in filenames:
                    if os.path.splitext(filename)[-1] in pcap_ext:
                        yield os.path.join(root, filename)
        elif os.path.isfile(pcappath):
            yield pcappath
    #二级############################################################

    #检查"输入：payload"格式，返回对应"协议类型"
    #二级##########################################################################################
    def app_proto_check(self, basic_proto, net_data):

        #分支1：tcp类型检查
        #三级#########################################################################################################################
        if basic_proto == "tcp":

            #如果检查时http协议，则返回"http"协议类型
            #四级#####################################
            try:
                dpkt.http.Request(net_data)
                return "http"
            #四级#####################################

            #否则，返回tcp协议类型，但有特殊情况
            #四级#####################################################################################
            except Exception as e:
                #特殊情况：“当http的请求头Content-Length 中的长度 和请求体的长度不相等时，dkpt会抛错，报错信息包含"short body"”,则返回"http"协议类型
                if type(e) == dpkt.dpkt.NeedData and "{}".format(e).find("short body") != -1:
                    return "http"
                return basic_proto
            #四级#####################################################################################

        #三级#########################################################################################################################

        #分支2：upd类型检查
        #三级#############################################################################################
        elif basic_proto == "udp":
            
            #如果符合dns协议格式，则返回"dns"协议类型
            #四级############################################################################################################
            try:
                dns = dpkt.dns.DNS(net_data)
                if dns.qr != dpkt.dns.DNS_Q:          #判断 DNS 报文是否为查询报文（即 qr 标志位是否为 0），dpkt.dns.DNS_Q为0
                    return basic_proto
                if dns.opcode != dpkt.dns.DNS_QUERY:  #判断操作码是否为标准查询（即 opcode 是否为 0），dpkt.dns.DNS_QUERY为0
                    return basic_proto
                if len(dns.qd) != 1:                  #检查 DNS 查询问题部分（qd）是否只有一条记录
                    return basic_proto
                if len(dns.an) != 0:                  #检查 DNS 回答资源记录部分（an）是否为空,Answer 部分包含了 DNS 查询请求所得到的回答
                    return basic_proto
                if len(dns.ns) != 0:                  #检查 DNS 授权资源记录部分（ns）是否为空,Authority 部分则包含了用于解析查询的权威服务器信息
                    return basic_proto
                if dns.qd[0].cls != dpkt.dns.DNS_IN:  #检查 DNS 查询问题部分（qd）的类（cls）是否为 IN 类
                    return basic_proto
                if dns.qd[0].type != dpkt.dns.DNS_A:  #检查 DNS 查询问题部分（qd）的类型（type）是否为 A 记录
                    return basic_proto
                return "dns"  #如果通过了所有检查，则说明输入的二进制数据符合 DNS 查询请求的标准形式
            #四级############################################################################################################

            #否则，返回"udp"协议类型
            #四级###########################
            except:
                return basic_proto
            #四级###########################

        #三级#############################################################################################

        #分支3：返回其他协议类型:icmp
        else:
            return basic_proto
        
    #二级##########################################################################################

    #输入：payload字节串(特征关键字)：b'def'，返回十六进制形式字符串：'64 65 66'
    #二级################################################################################
    def str2hexstr(self, buf):
        return ' '.join(['%02x' % x for x in buf])
    #二级################################################################################

    #输入时间戳，否则，为当前时间，并返回
    #二级##################################################################
    def timestamp2date_d(self,time_stamp="",format_string="%Y%m%d"):
        if not time_stamp:
            time_stamp = time.time()
        time_array = time.localtime(time_stamp)
        str_data = time.strftime(format_string,time_array)
        return str_data
    #二级##################################################################
   
    #输入:snort规则，输出:md5值,解释：未写入文件前，计算其字节序列md5值,即为snort文件md5值
    #二级##########################################################
    def md5_calculator_str(self,str_obj):
        str_obj = bytes(str_obj,encoding="utf-8")
        md5_obj = hashlib.md5()
        md5_obj.update(str_obj)
        hash_code = md5_obj.hexdigest()
        md5 = str(hash_code).lower()
        return md5
    #二级##########################################################

    #输入"payload"、"初判协议类型"(没用到)，"检查后的协议类型"，将"感兴趣的payload"增加至rule字典，并返回
    #二级##########################################################################################################################################
    def matching(self, net_data, basic_proto, app_proto):

        #使用 items() 方法获取"规则策略"字典中所有键值对
        #三级##########################################################################################################################
        for rulename, rule in self.policy.items():

            if rule.get("proto") != app_proto:                    #跳过其他协议的，留下匹配的协议继续任务
                continue
            rule_max_len = rule.get("offset") + rule.get("depth") #"偏移量+深度"作为规则payload部分的长度
            if rule_max_len > len(net_data):                      #排除："规则payload部分的长度"大于整个包的情况
                continue
            elif rule_max_len == 0 and rule.get("keywords") == []: #排除：没有定位，没有"特征关键字"情况
                continue

            #不变 rule.get("keywords") == []
            # 情况1：rule_max_len<0 rule.get("keywords") == []（小概率）
            # 情况2：rule_max_len>0 rule.get("keywords") == []（有定位。没有"特征关键字"）
            #不变 rule_max_len == 0
            # 情况3：rule_max_len == 0 rule.get("keywords")! =[](没有定位，有"特征关键字")
            #都变
            # 情况4：rule_max_len<0  le.get("keywords")! =[]  （小概率）情况2
            # 情况5：rule_max_len>0 rule.get("keywords")! =[] （都有）
            #四级##################################################################################################################
            else:
                #获取"特征关键字"个数
                #五级###################################################################
                keywords_count = rule.get(
                    "keywords_count").split("of")[0].strip()
                if keywords_count == "all":
                    keywords_count = len(rule.get("keywords"))
                keywords_count = int(keywords_count)
                #五级###################################################################

                #分流1：没有"特征关键字",情况1（小概率）、情况2（有定位。没有"特征关键字"），并返回
                #五级#############################################################################################################
                if not rule.get("keywords"):
                    if rule_max_len > 0:  #即：情况2（有定位。没有"特征关键字"），并返回
                        rule["snort_item"] = {}
                        rule["snort_item"][self.str2hexstr(net_data[rule.get("offset"):rule.get("offset") + rule.get("depth")])] = None
                        return rule
                    else:  #即：情况1（小概率），并返回
                        return {}
                #五级#############################################################################################################


                #剩下：情况3(没有定位，有"特征关键字")、情况5（都有）和情况4（小概率），将"特征关键字"增加至rule字典，并返回
                ####################################################################################################################
                
                #如果是情况5（都有），则截取payload
                #五级################################################################################
                if rule_max_len > 0:
                    net_data = net_data[rule.get("offset"):rule.get("offset") + rule.get("depth")]
                #五级################################################################################

                #最后，情况3和情况5 将"特征关键字"增加至rule字典，并返回
                #五级######################################################################
                rule["snort_item"] = {};flag_count = 0      #预定义："特征关键字"存储容器:rule{...,'snort_item':{xx:xx}}；"状态变量"
                for word in rule.get("keywords"):
                    if net_data.find(word.encode()) == -1:  #过滤：如果该"特征关键字"不在payload里，则跳过
                        continue
                    hexstr = self.str2hexstr(word.encode()) #预处理："特征关键字"->"十六进制形式字符串"的特征关键字
                    if hexstr in rule["snort_item"]:        #如果"十六进制形式字符串"的特征关键字，已经存在，则跳过
                        continue
                    rule["snort_item"][hexstr] = None       #执行："十六进制形式字符串"的特征关键字,作为键新增至rule{...,'snort_item':{xx xx:None}}
                    flag_count += 1                         #状态记录
                    if flag_count == keywords_count:        #当所有关键字都被新增时，则返回rule{}
                        return rule
                #五级######################################################################
                ####################################################################################################################

            #四级##################################################################################################################  
        return {}
        #三级##########################################################################################################################

    #二级##########################################################################################################################################

    
    #输入rule字典，写入snort规则文件,snort规则拆分为四部分，1.rule_header,2.rule_msg,3.rule_body(payload),4.rule_classify
    #二级#######################################################################################################################################
    def snort_out(self, rule_data: dict):
        rule_header = "alert %s any any -> any any "%(rule_data.get("proto")) #1.rule_header部分
        
        rule_msg = '''msg:"{'org': '', 'author': 'snort_tools', 'behavior': ['%s'], 'vulnerability_id': '%s', 'app_info': '%s', 'description': '%s', 'extract_date': '%s', 'threat_name': '', 'family': '%s', 'sign_source': 'ArtificialExtraction', 'refer': []}";'''%(rule_data.get("behavior"),rule_data.get("cve_num"),rule_data.get("app_info"),rule_data.get("description"),self.timestamp2date_d(),rule_data.get("family"))  #2.rule_msg部分

        #3.rule_body(payload)部分
        #三级########################################################
        rule_body = ''''''
        if rule_data.get("snort_item"):
            for key,value in rule_data.get("snort_item").items():
                rule_body +='''content:"|%s|";'''%(key)
        else:
            return
        #三级########################################################


        rule_classify = '''classtype:%s;'''%(rule_data.get("classify")) if rule_data.get("classify") else "" #4.rule_classify部分
        
        snort_info = "{}({}{}{})".format(rule_header,rule_msg,rule_body,rule_classify)  #将四个部分组合
        
        #写入规则文件
        #三级#############################################################################################################
        with open(os.path.join(self.snortlib,"snort_{}.rules".format(self.md5_calculator_str(snort_info))),"wb")  as fw:
            fw.write(bytes(snort_info,encoding="utf-8"))
        #三级#############################################################################################################

    #二级#######################################################################################################################################


    #输入实例对象，类型：<class 'dpkt.pcap.Reader'>，没有返回值
    #二级#######################################################################################################################################
    def analysis(self, pcap: dpkt.pcap.Reader) -> dict:

        if not isinstance(pcap, dpkt.pcap.Reader):  #用于判断变量 pcap 是否是 <class 'dpkt.pcap.Reader'>类型的实例对象。如果 pcap 不是,则抛出异常
            raise "parameter pcap need dpkt.pcap.Reader"

        #常规操作(pcap是迭代器)：遍历读取pcap文件中的每个数据包，ts：(<class 'float'>)表示时间戳，buf：(<class 'bytes'>)则是对应的二进制数据
        #三级###################################################################################################################################
        for ts, buf in pcap:
            eth = dpkt.ethernet.Ethernet(buf)  #buf解析为Ethernet数据帧，引dpkt库ethernet模块Ethernet类，构建+初始化“实例对象”，二进制数据流->实例对象
            if not isinstance(eth.data, dpkt.ip.IP):#检查eth.data对象是否属于dpkt.ip.IP类或（即IP数据包），若不是，则跳过当前循环迭代进行下一个迭代。
                continue
            ip = eth.data                         #从以太网帧对象 eth 中获取 IP 数据报（IP datagram）。此时，变量 ip 包含了一个 IP 数据报对象。

            #检查是否是icmp包
            #四级##################################################################################################################
            if isinstance(ip.data, dpkt.icmp.ICMP):
                icmp = ip.data                 #从 IP 数据报对象 ip 中获取 ICMP 报文（ICMP message）。此时，变量 icmp 包含了一个 ICMP 报文对象。
                icmp_operate = icmp.data       #从 ICMP 报文对象 icmp 中获取了 ICMP 协议操作,即：“ICMP报文包括报头和数据”中的数据字段部分，
                if not isinstance(icmp_operate, dpkt.icmp.ICMP.Echo):
                    continue
                if len(icmp_operate.data) > 0:  #'icmp_operate.data'可获得数据字段部分的具体数据，即：payload
                    ret = self.matching(icmp_operate.data, "icmp", self.app_proto_check("icmp", icmp_operate.data))
                    self.snort_out(ret)
            #四级##################################################################################################################

            #检查是否是tcp包
            #四级############################################################################
            elif ip.p == dpkt.ip.IP_PROTO_TCP:
                tcp = ip.data
                if len(tcp.data) > 0:
                    ret = self.matching(
                        tcp.data, "tcp", self.app_proto_check("tcp", tcp.data))
                    self.snort_out(ret)
                else:
                    pass
            #四级############################################################################

            #检查是否是udp包
            #四级###########################################################################
            elif ip.p == dpkt.ip.IP_PROTO_UDP:
                upd = ip.data
                if len(upd.data) > 0:
                    ret = self.matching(
                        upd.data, "udp", self.app_proto_check("udp", upd.data))
                    self.snort_out(ret)
                else:
                    pass
            #四级###########################################################################
        #三级###################################################################################################################################
    #二级#######################################################################################################################################
#一级###########################################################################################################################################


#程序入口
#一级##################################################################################################################################
def main():
    args = cmdlineparser()  #命令行解析对象

    p2s = Pcap2Snort()                         #步1：{“任务：分析Pcap，输出snort规则”类 实例化对象}->p2s
    p2s.load_policy()                          #步2：p2s导入“规则策略配置”
    for filepath in p2s.load_pcap(args.pcap):  #步3：遍历每个pcap文件
        with open(filepath, 'rb') as f:        #步4：获取pcap文件句柄
            p2s.analysis(dpkt.pcap.Reader(f))  #步5：1）“pcap文件句柄”转换为'dpkt.pcap.Reader'的对象，2）传入该参数,p2s开始分析任务
#一级##################################################################################################################################


if __name__ == '__main__':
    main()
