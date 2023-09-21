# coding=utf-8
import sys,json,time,datetime,os,zipfile
from os.path import basename

import elasticsearch
from ssl import create_default_context

#类：列构造获取ES客户端的类
#一级##################################################################################################################
class ElasticSearchClient(object):
    
    #构造函数
    def __init__(self,is_authorization=False) :
        self.is_authorization = is_authorization   #“是否做身份验证”信标

    #获取es客户端实例
    #二级######################################################################################################
    def get_es_servers(self):
        
        #连接es,需要验证
        #三级########################################################################
        if self.is_authorization:

            try:
                #连接es
                es_client = elasticsearch.Elasticsearch(['https://es-3ylk2io1.public.tencentelasticsearch.com:9200'],http_auth=('elastic', '879086359@QQ.com'),)
                
                ###################测试连接是否成功#######################
                # try:
                #     health = es_client.cluster.health()
                #     print("连接成功！")
                #     print(json.dumps(health,indent=2))

                # except Exception as e:
                #     print("连接失败。错误信息:", e)
                #########################################################

                return es_client

            except Exception as err:
                print(err)
                return None
        #三级########################################################################

        #连接es不需要身份验证
        #三级########################################################################
        else:

            es_servers = [{
                "host":"es-3ylk2io1.public.tencentelasticsearch.com",
                "port":"9200"
            }]
            try:
                es_client = elasticsearch.Elasticsearch(hosts=es_servers)
                return es_client
            except Exception as err:
                print(err)
                return None
        #三级########################################################################
    #二级######################################################################################################
#一级##################################################################################################################


#es客户端实例化
es_client = ElasticSearchClient(is_authorization=True).get_es_servers()

#是否压缩信标，默认否
is_compress = False

#当前的时间：2023-09-18 10:22:27
time_now_format = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

#当前时间的开始时间：2023-09-18 00:00:00
today_format_start = time_now_format.split()[0] + ' 00:00:00'

#前一天的当前时间
yestoday_now_format = datetime.datetime.fromtimestamp(time.time() - 24 * 60 * 60).strftime('%Y-%m-%d %H:%M:%S')

#前一天的开始时间:xxxx-xx-xx 00:00:00
yestoday_format_start = yestoday_now_format.split()[0] + ' 00:00:00'

#时间戳（前一天的开始时间:xxxx-xx-xx 00:00:00）
yestoday_timestamp_start = int(time.mktime(time.strptime(yestoday_format_start, '%Y-%m-%d %H:%M:%S')))


#前一天的结束时间:xxxx-xx-xx 23:59:59
yestoday_format_end = yestoday_now_format.split()[0] + ' 23:59:59'

#时间戳（前一天的结束时间:xxxx-xx-xx 23:59:59）
yestoday_timestamp_end = int(time.mktime(time.strptime(yestoday_format_end, '%Y-%m-%d %H:%M:%S')))

#前一天的日期
out_put_dir_time = datetime.datetime.fromtimestamp(time.time() - 24 * 60 * 60).strftime('%Y-%m-%d')

dir_path = 'result'

#默认index为：'test_alert'
index_global = 'test_alert'


# 获取参数：
# 第一步：index (es索引名称)
# 第二步：source_key（接收需要导出的字段）
# 第三步：（开始时间）
# 第四步：（结束时间）
# 第五步：must_query_list（过滤条件列表）
# 第六步：distinct_key（要去重的字段列表）
# 第七步：is_compress（是否压缩导出信标）
#一级##################################################################################################################
def get_input():
    
    #帮助说明
    #########################################################################################################
    pre_alert = """
    1. 导出攻击者IP（只要IP）
    运行：python output_data.py, 第二步输入: attacker_ip

    2. 导出DDOS攻击类型需要数据：攻击者IP、端口、协议、家族、payload
    运行：python output_data.py, 第二步输入: attacker_ip src_port dest_port proto alert.signature.family payload
    第五步输入：过滤字段: alert.category.keyword, 过滤值: 拒绝服务攻击

    3.根据event_hash去重后导出
    运行：python output_data.py，第六步输入去重event_hash
    """
    print(pre_alert)
    #########################################################################################################

    #第一步：接收index，es的索引名称
    ################################################
    while True:
        index = input("第1步:请输入取数据的index:")  #接收数据
        if es_client.indices.exists(index=index):   #是否在es数据库中存在，存在则跳出循环
            break
        else:
            print("输入的index不存在")
    ################################################
    
    #第二步：接收需要导出的字段，导出所有：*
    #################################################################################################################################################
    source_key = input('第2步:请输入导出字段(导出全部: *，导出源ip: src_ip, 导出目的ip: dest_ip, 导出域名: dns.rrname,等等，如需导出多个，请用空格分隔): ')
    source_key = source_key.split()
    #################################################################################################################################################

    #第三步：接收开始时间，如：2023-09-18 00:00:00，并转换为时间戳
    ###########################################################################################
    while True:
        time_start = input('第3步:请输入开始时间(格式：%s):' % (today_format_start,))
        try:
            timestamp_start = int(time.mktime(time.strptime(time_start, '%Y-%m-%d %H:%M:%S')))
        except:
            print('输入错误...')
        else:
            break
    ###########################################################################################

    #第四步：接收结束时间，如：2023-09-18 16:41:27，并转换为时间戳
    ###########################################################################################
    while True:
        time_end = input('第4步:请输入结束时间(格式：%s):' % (time_now_format,))
        try:
            timestamp_end = int(time.mktime(time.strptime(time_end, '%Y-%m-%d %H:%M:%S')))
        except:
            print('输入错误...')
        else:
            break
    ###########################################################################################

    #第五步：接收过滤条件信标，如：n
    #####################################################################################
    is_filter = input('第5步:是否增加其他过滤条件，如攻击类型, y/n:')  #确定是否增加过滤条件
    is_filter = is_filter.lower()                                   #转为小写
    match_query = ''
    if is_filter == 'y' or is_filter == 'yes':                     #如果为增加过滤条件
        query_key = input('请输入过滤字段：')                       #则接收：过滤字段
        query_value = input('请输入过滤值：')                       #则接收：过滤值
        match_query = {                                            #保存为字典  
            "term": {
                query_key + '.keyword': query_value
            }
        }

    must_query_list = []
    if match_query:                                                #存储为列表形式
        must_query_list.append(match_query)
    #####################################################################################

    #第六步：接收是否去重后导出信标，如：n
    #####################################################################################
    is_distinct = input('第6步:是否去重后导出,如根据event_hash去重后导出，y/n:')
    is_distinct = is_distinct.lower()                                   #转为小写
    distinct_key = []
    if is_distinct == 'y' or is_distinct == 'yes':                      #如果需要去重
        distinct_key = input('请输入去重字段(如需多字段去重，空格分隔):') #则接收需要去重的字段，多字段空格分隔
        distinct_key = distinct_key.split()                             #则存储为列表形式
    #####################################################################################

    #第七步：接收是否压缩导出信标，如：y
    #####################################################################################
    is_compress = input('第7步:是否压缩导出，y/n:')
    is_compress = is_compress.lower()
    if is_compress == 'y' or is_compress == 'yes':
        is_compress = True
    else:
        is_compress = False
    #####################################################################################

    print('开始导出。。。')
    
    #共七个参数返回
    return index,timestamp_start,timestamp_end,source_key,must_query_list,distinct_key,is_compress
#一级##################################################################################################################

#情况1：如果有需要“去重的字段列表”:distinct_key
#一级####################################################################################################################
def aggs_search(index, time_start, time_end, data_file, source_key, must_not_query, must_query_list, distinct_key):


    timestamp = "timestamp"
    
    #暂时不管
    #############################################################################################
    if index == 'sandbox':
        timestamp = "@timestamp"
        time_start -= 8 * 60 * 60
        time_start = str(datetime.datetime.fromtimestamp(time_start).strftime('%Y-%m-%dT%H:%M:%S'))
        time_end -= 8 * 60 * 60
        time_end = str(datetime.datetime.fromtimestamp(time_end).strftime('%Y-%m-%dT%H:%M:%S'))
    #############################################################################################

    #构建了一个es查询字典
    #二级######################################################################################################
    query_dict = {
        "size": 0,
        "query": {
            "bool": {
                "filter": {
                    "range": {
                        timestamp: {
                            "gte": time_start,                    #传入参数time_start：开始时间
                            "lte": time_end                       #传入参数time_end：结束时间参数
                        }
                    }
                },
                "must_not": must_not_query,                       #传入参数must_not_query：指定哪些条件不匹配列表
                "must": must_query_list                           #传入参数must_query_list：过滤条件列表
            }
        },
        "aggs": {
            "term_by_key": {
                "terms": {
                    "script": {
                        #如：distinct_key=["a","b"]，则："source": "return doc['a.keyword'].value+doc['b.keyword'].value"
                        "source": "return " + '+'.join(map(lambda item: 'doc[\'' + item + '.keyword\'].value', distinct_key))  #传入参数distinct_key：需要去重的字段列表
                    },
                    "size": 10000000
                },
                "aggs": {
                    "top_by_key": {
                        "top_hits": {
                            "size": 1,
                            "_source": source_key              #传入参数source_key：需要导出的字段列表
                        }
                    }
                }
            }
        }
    }
    #二级######################################################################################################

    #如果不存在"C:\\Users\\Administrator\\Desktop\\IDS_output_data\\result"目录，则创建
    if not os.path.isdir(os.path.dirname(data_file)):
        os.mkdir(os.path.dirname(data_file))

    #写方式打开：'C:\Users\Administrator\Desktop\IDS_output_data\test_alert--2023-09-19T11:26:17.json' 文件
    f = open(data_file,'w')


    #打印es查询字典
    print(json.dumps(query_dict)) #或print(json.dumps(query_dict,indent=2))

    #使用es_client执行搜索操作，index：指定索引，doc_type：指定搜索文档类型，body:领域特定语言(DSL)的查询描述,request_timeout：请求的超时时间
    res_data = es_client.search(index=index, doc_type='doc', body=query_dict, request_timeout=300)

    res_data_buckets = res_data['aggregations']['term_by_key']['buckets']

    #处理搜索结果并存储
    #二级#############################################################################
    
    #指定字段：source_key，导出数据
    if len(source_key) == 1 and source_key[0] != '*':
        value_set = set()
        source_key = source_key[0].split('.')
        for data in res_data_buckets:
            data = data['top_by_key']['hits']['hits'][0]
            try:
                if len(source_key) > 1:
                    source_value = data['_source']

                    for key in source_key:
                        source_value = source_value[key]
                else:
                    source_value = data['_source'][source_key[0]]
                value_set.add(source_value)
            except Exception as e:
                print (e)
        value_list = list(value_set)
        f.write(json.dumps(value_list))
    #导出所有数据
    else:
        for data in res_data_buckets:
            data = data['top_by_key']['hits']['hits'][0]
            f.write(json.dumps(data['_source']))
            f.write('\n')
    f.close()
    #二级#############################################################################
#一级####################################################################################################################

#情况2：没有需要“去重字段列表”
#一级############################################################################################################
def scroll_search(index, time_start, time_end, data_file, source_key, must_not_query, must_query_list):
    
    timestamp = "timestamp"
    
    #暂时不管
    #############################################################################################
    if index == 'sandbox':
        timestamp = '@timestamp'
        time_start -= 8 * 60 * 60
        time_start= str(datetime.datetime.fromtimestamp(time_start).strftime('%Y-%m-%dT%H:%M:%S'))
        time_end -= 8 * 60 * 60
        time_end = str(datetime.datetime.fromtimestamp(time_end).strftime('%Y-%m-%dT%H:%M:%S'))
    #############################################################################################

    query_dict = {
        "size": 2000,
        "query": {
            "bool": {
                "filter": {
                    "range": {
                        timestamp: {
                            "gte": time_start,           #传入参数time_start：开始时间
                            "lte": time_end              #传入参数time_end：结束时间参数
                        }
                    }
                },
                "must_not": must_not_query,             #传入参数must_not_query：指定哪些条件不匹配列表
                "must": must_query_list                 #传入参数must_query_list：过滤条件列表
            }

        },
        "_source": source_key                            #传入参数source_key：需要导出的字段列表
    }

    #如果不存在"C:\\Users\\Administrator\\Desktop\\IDS_output_data\\result"目录，则创建
    if not os.path.isdir(os.path.dirname(data_file)):
        os.mkdir(os.path.dirname(data_file))

    #写方式打开：'C:\Users\Administrator\Desktop\IDS_output_data\test_alert--2023-09-19T11:26:17.json' 文件
    f = open(data_file,'w')
    
    #打印es查询字典
    print(json.dumps(query_dict))

    #使用es_client执行搜索操作，index：指定索引，doc_type：指定搜索文档类型，body:领域特定语言(DSL)的查询描述,scroll:滚动上下文的超时时间,request_timeout：请求的超时时间
    res_data = es_client.search(index=index,doc_type='doc',body=query_dict,scroll='2m',request_timeout=20)

    #搜索中获取了多少个文档
    scroll_size = len(res_data['hits']['hits'])
    
    #处理搜索结果并存储
    #二级#############################################################################
    
    #指定字段：source_key，导出数据
    if len(source_key) == 1 and source_key[0] != '*':
        value_set = set()
        source_key = source_key[0].split('.')
        while scroll_size > 0:
            _scroll_id = res_data['_scroll_id']
            data_list = res_data['hits']['hits']   # 查到的数据在这儿
            for data in data_list:
                try:
                    if len(source_key) > 1:
                        source_value = data['_source']

                        for key in source_key:
                            source_value = source_value[key]

                    else:
                        source_value = data['_source'][source_key[0]]
                    value_set.add(source_value)
                except Exception as e:
                    print(e)
            res_data = es_client.scroll(scroll_id=_scroll_id,scroll='2m')
            scroll_size = len(res_data['hits']['hits'])
        value_list = list(value_set)
        f.write(json.dumps(value_list))
    
    #导出所有数据
    else:
        while scroll_size > 0:
            _scroll_id = res_data['_scroll_id']
            data_list = res_data['hits']['hits']  # 查到的数据在这儿
            for data in data_list:
                f.write(json.dumps(data['_source']))
                f.write('\n')
            res_data = es_client.scroll(scroll_id=_scroll_id, scroll='2m')
            scroll_size = len(res_data['hits']['hits'])
    f.close()
    #二级#############################################################################
#一级############################################################################################################


#日志记录
################################################################################################
def save_record(index, time_start, time_end, data_file, source_key, compress=False):
    time_start = datetime.datetime.fromtimestamp(time_start).strftime('%Y-%m-%dT%H:%M:%S')
    time_end = datetime.datetime.fromtimestamp(time_end).strftime('%Y-%m-%dT%H:%M:%S')
    record_file = 'C:\\Users\\Administrator\\Desktop\\IDS_output_data\\record.txt'
    if not os.path.isfile(record_file):
        temp_file = open(record_file,'w')
        temp_file.close()

    with open(record_file,'a') as f:
        record_string = ' 操作时间: ' + time_now_format + ' index:' + index + ' 开始时间: ' + time_start + ' 结束时间: ' + time_end + ' 导出字段:' + str(source_key) + ' 生成文件: ' + data_file 
        f.write(record_string + '\n')
    print('数据已保存至文件：%s' % (data_file))
################################################################################################

#压缩为压缩包
###########################################################################
def compress_file(data_file):
    try:
        compression = zipfile.ZIP_DEFLATED
    except:
        compression = zipfile.ZIP_STORED
    zip_file = data_file.replace('.json','.zip')
    zf = zipfile.ZipFile(zip_file,mode='w',allowZip64=True)
    try:
        zf.write(data_file,basename(data_file),compress_type=compression)
    except Exception as e:
        print(e)
    finally:
        zf.close()
        os.remove(data_file)
        print('删除: %s，生成压缩文件: %s' % (data_file, zip_file))
###########################################################################

#函数入口
if __name__ == '__main__':
    
    #如果命令行已存在完整参数，则进入
    #####################################################################################################################################
    if len(sys.argv) == 9:
        
        #是否压缩信号
        is_compress == True

        #从命令行获取参数值，8个
        index_global, time_start_global, time_end_global,dir_path, source_key_global,must_not_query_list_global, must_query_list_global, distinct_key_global =sys.argv[1:]

        #有些参数需要转换格式
        ##################################################################
        time_start_global = int(time_start_global)
        time_end_global = int(time_end_global)
        source_key_global = json.loads(source_key_global)
        must_not_query_list_global = json.loads(must_not_query_list_global)
        distinct_key_global = json.loads(distinct_key_global)
        ##################################################################

        
        if time_start_global == -1 and time_end_global == -1:
            time_start_global = yestoday_timestamp_start
            time_end_global = yestoday_timestamp_end


        #'C:\Users\Administrator\Desktop\IDS_output_data\result\test_alert--2023-09-03.json'
        data_file_global = 'C:\\Users\\Administrator\\Desktop\\IDS_output_data\\' + dir_path + '\\%s' % (index_global + '--' + out_put_dir_time + '.json')
    #####################################################################################################################################

    #否则，交互式获取参数
    #####################################################################################################################################
    else:
        #es索引名称、开始时间、结束时间、接收需要导出的字段列表、过滤条件列表、要去重的字段列表、是否压缩导出信标
        index_global, time_start_global, time_end_global, source_key_global, must_query_list_global, distinct_key_global, is_compress = get_input()
        
        #指定哪些条件不匹配列表
        must_not_query_list_global = []
        
        dir_path = ''
        
        #'C:\Users\Administrator\Desktop\IDS_output_data\test_alert--2023-09-19T11:26:17.json'
        data_file_global = 'C:\\Users\\Administrator\\Desktop\\IDS_output_data\\%s' %(index_global + '--' + time_now_format.replace(' ','T') + '.json')
    #####################################################################################################################################

    #如果不存在路径：'C:\\Users\\Administrator\\Desktop\\IDS_output_data\\',则创建
    if os.path.exists('C:\\Users\\Administrator\\Desktop\\IDS_output_data\\') != True:
        os.system('md C:\\Users\\Administrator\\Desktop\\IDS_output_data')

    #如果有需要“去重的字段列表”
    if distinct_key_global:
        aggs_search(index_global, time_start_global, time_end_global, data_file_global, source_key_global,must_not_query_list_global,must_query_list_global, distinct_key_global)
    
    #否则，没有需要“去重字段列表”
    else:
        scroll_search(index_global, time_start_global, time_end_global, data_file_global, source_key_global,must_not_query_list_global,must_query_list_global)
    
    #日志记录
    save_record(index_global, time_start_global, time_end_global, data_file_global, source_key_global)
    
    
    #开始压缩
    if is_compress:
        compress_file(data_file_global)






