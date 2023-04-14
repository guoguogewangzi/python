import re
'''
# 匹配上的第一个
re.search(regex, text)
# 所有匹配的
re.findall(regex, text)
# 替换所有匹配的
r = re.sub(regex, a, text)
'''

#元字符
'''
代码        说明
.           匹配除换行符以外的任意字符
\d          匹配任意数字
\D          匹配任意非数字
\w          匹配任意字母数字下划线
\W          匹配任意非字母数字下划线 
\s          匹配任意空白字符
\S          匹配任意非空白字符
'''

#量词
'''
符号        说明
*           0到多次
+           1到多次
?           0到1次
{m}         出现m次
{m,}        出现至少m次 {m,n} m到n次
'''

#范围
'''
符号 说明
|               或，如何ab|bc
[...]           多选一，括号中的任意个字符
[a-z]           匹配a到z的字母
[0-9]           匹配0到9的数字
[\^...]         取反，不是括号中的任意一个字符
'''



#分支的优先级
'''
这里我们可以类比Python中的逻辑运算符`or`。当第一个条件已经满足匹配结果时，会直接返回第一个作为结果。如果想要使这个正则表达式按照预期运行，我们怎么改呢？
'''
'''
回答：
将字符多的匹配结果放在前面，就会优先去匹配`https`。
'''
# text1 = "http://www.baidu.com"
# text2 = "https://www.baidu.com"
# #regex = r"http|https"改为：
# regex = r"https|http"
# r1= re.search(regex, text1)
# r2= re.search(regex, text2)
# print('')


#分组
'''
符号        说明
(...)       对正则语法进行分组
'''
# text1 = "https://www.baidu.com"
# text2 = "http://www.baidu.com"
# text3 = "ftp://www.baidu.com/oiajdg.zip"
# #regex = r"https?|ftp://www.baidu.com"   #改为：
# regex = "(https?|ftp)://www.baidu.com"
# r1=re.search(regex, text1)                 # 匹配结果：https
# r2=re.search(regex, text2)                 # 匹配结果：http
# r3=re.search(regex, text3)                 # 匹配结果：ftp://www.baidu.com 
# print('')

#引用
'''
被分组的正则表达式除了表示一个整体外，还能够提取匹配到的
文本内容。我们可以通过\+从1递增的数字编号来获取。下面示例
中，我们通过使用引用的方式来匹配重复出现的单词。
'''

text = "abb"
regex = r"(a)(b)\2"
r1= re.search(regex, text)
print('')