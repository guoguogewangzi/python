# https://es-3ylk2io1.public.tencentelasticsearch.com:9200
# elastic
# *******
# curl -XGET 'https://es-3ylk2io1.public.tencentelasticsearch.com:9200' -H 'Content-Type: application/json'  -u elastic:*******
# curl -XGET 'https://es-3ylk2io1.public.tencentelasticsearch.com:9200/_cat/health?v' -H 'Content-Type: application/json'  -u elastic:*******
# curl -XGET 'https://es-3ylk2io1.public.tencentelasticsearch.com:9200/_cat/indices?v' -H 'Content-Type: application/json'  -u elastic:*******

# curl -XGET 'https://es-3ylk2io1.public.tencentelasticsearch.com:9200/china/_doc/beijing?pretty' -H 'Content-Type: application/json'  -u elastic:*******

# curl -XDELETE 'https://es-3ylk2io1.public.tencentelasticsearch.com:9200/my_index?pretty' -H 'Content-Type: application'  -u elastic:*******

# curl -XDELETE 'https://es-3ylk2io1.public.tencentelasticsearch.com:9200/china/_doc/beijing?pretty' -H 'Content-Type: application/json'   -u elastic:*******

#第三方库
# from elasticsearch import Elasticsearch


#连接es
#########################################################################################################
# es = Elasticsearch(["https://es-3ylk2io1.public.tencentelasticsearch.com:9200"],
#                    http_auth=('elastic', '*******'),
#                    sniff_on_start=False,
#                    sniff_on_connection_fail=False,
#                    sniffer_timeout=None)
#########################################################################################################

# 测试连接
#########################################################################################################
# import json
# try:
#     health = es.cluster.health()
#     print("连接成功！")
#     print(json.dumps(health,indent=2))

# except Exception as e:
#     print("连接失败。错误信息:", e)
#########################################################################################################


# 插入/更新数据
#########################################################################################################
# res = es.index(index="my_index",  id=3, body={"title": "Two", "name":"zhangsan","tags": ["ruby"]})
# print(res)
#########################################################################################################


# 查询数据
#########################################################################################################
# res = es.get(index="my_index", id=3)
# print(res['_source'])
#########################################################################################################


# 删除单个文档
#########################################################################################################
# es.delete(index='my_index',id=3)
#########################################################################################################


# distinct_key=["a","b"]
# test = "return " + '+'.join(map(lambda item: 'doc[\'' + item + '.keyword\'].value', distinct_key))
# print(test)


# def square(x):
#     return x**2

# my_list = [1, 2, 3, 4, 5]

# result = map(square, my_list)
# result_list = list(result)

# print(result_list)


# add = lambda item: 'doc[\'' + item + '.keyword\'].value'
# result = add("ggg")
# print(result)

