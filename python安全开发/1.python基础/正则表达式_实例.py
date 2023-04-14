import re

#2021年07月11日 19时19分00秒

#利用python语法方式替换：就是取值
# test='今天是个特殊的日子2021-07-11 19:19:00 的点点滴滴'
# result = re.search(r'(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})',test)
# print(result.groups())
# print(result[0])
# print(f'{result[1]}年{result[2]}月{result[3]}日 {result[4]}时{result[5]}分{result[6]}秒')

#利用正则的方式替换，分组:(),并引用:\num
# test = '今天是个特殊的日子2021-07-11 19:19:00 的点点滴滴'
# result = re.sub(r'(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})',r'\1年\2月\3日 \4时\5分\6秒',test)
# print(result)

#命名分组:?P<year>
# test='今天是个特殊的日子2021-07-11 19:19:00 的点点滴滴'
# result = re.search(r'(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2}) (\d{2}):(\d{2}):(\d{2})',test)
# print(result.group(1))                        #取值方式一
# print(result.group("month"))                  #取值方式二
# print(result['day'])                          #取值方式三
# print(result[0])
# print(result.group(0))

'''
贪婪模式，是最大值匹配。而非贪婪模式，就是最小值匹配。
默认情况下贪婪模式，通过在量词后面加上?，可以启用非贪婪模式。
'''
#默认贪婪模式：
text = "请在下列选项中选出正确答案(B) (A)地方不大方便(B)怪怪的风格"
result = re.search(r'\(.+\)',text)
print(result[0])

#非贪婪模式：加一个：? 就可以;flags=re.IGNORECASE:忽略英文大小写匹配
text = "请在下列选项中选出正确答案(B) (A)地方不大方便(B)怪怪的风格"
result = re.search(r'\(.+?\)',text,flags=re.IGNORECASE)
print(result[0])