import re

#re.search()用法
match = re.search(r'[1-9]\d{5}', 'BIT 100081')
if match:
    print("re.search():",match.group(0))

#re.mathc()的用法
# 会出错
# match = re.match(r'[1-9]\d{5}', 'BIT 100081')
# if match:
#     print(match.group(0))
# match.group(0)

# match = re.match(r'[1-9]\d{5}', '100081 BIT')
# if match:
#     print(match.group(0),type(match))

#re.findall()的用法
ls = re.findall(r'[1-9]\d{5}', 'BIT100081 TSU100081')
print(ls)

#re.split()用法
# print(re.split(r'[1-9]\d{5}', 'BIT100081 TSU100081'))
# print(re.split(r'[1-9]\d{5}', 'BIT100081 TSU100081 '))
# print("1,2,3,4,5".split(","))
# print("1,2,3,4,5,".split(","))
# print(re.split(r'[1-9]\d{5}', 'BIT100081 TSU100081',maxsplit=1))

#re.finditer的用法
# for m in re.finditer(r'[1-9]\d{5}', 'BIT100081 TSU100084'):
#     if m:
#         print(m.group(0))

#re.sub的用法
# print(re.sub(r'[1-9]\d{5}', ':zipocde', 'BIT100081 TSU100084'))

#re.compile()用法
resg=re.compile(r'[1-9]\d{5}')
print(resg.search('BIT100081 TSU100084').group(0))


#实战：

#统计ip个数
regex = r"(?:\b25[0-5]|\b2[0-4][0-9]|\b[01]?[0-9][0-9]?)(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}" #知识点：?:类似 (...), 但是不表示一个组；因为用findall()匹配时，会只取分组的内容，用"?:"来取消，取所有内容。?:在有分组的情况下findall()函数，不只拿分组里的字符串，拿所有匹配到的字符串

text = "172.20.80.10,172.20.80.11,172.20.80.31,172.20.80.32,172.20.80.33,172.20.80.34,172.20.80.41,172.20.80.42,172.20.80.43,172.20.80.45,172.20.80.46,172.20.80.47,172.20.80.48,172.20.80.49,172.20.80.51,172.20.80.52,172.20.80.53,172.20.80.55,172.20.80.57,172.20.80.63,172.20.80.64,172.20.82.70,172.20.82.187,172.20.82.188"

res = re.findall(regex,text)

print(res,len(res))