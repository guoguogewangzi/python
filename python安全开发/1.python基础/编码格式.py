'''
字符 十六进制 十进制 二进制
这四个之间的关系一定要搞清楚
1、特殊字符一般用"\x00" 十六进制表示


'''


# import base64

# #ASCII码
# print('------------ASCII码--------------')
# print(ord('a'))      #ord()查看字符'a'的ASCII码     ord()：查看字符的ascii码(表现形式：十进制，十六进制)
# print(chr(97))        #chr()查看97 ASCII码，对应的字符     chr():查看ascii码(表现形式：十进制，十六进制) 对应的字符
# print()

# #utf-8,gbk编码
# print('------------utf-8,gbk编码--------------')
# str='www.baidu.com'
# str2='张鑫'
# print(str.encode('utf8'))   
# print(str.encode('gbk'))
# print(str2.encode('utf8') )  #打印utf-8编码的码号
# print(str2.encode('gbk'))  #打印gbk编码的码号
# print()

# #Unicode编码
# print('------------Unicode编码--------------')
# print(hex(ord('鑫')))       #ord()可以查看ASCII码，也是Unicode码（Unicode的前部分就是ASCII值）,hex()十六进制的形式查看码位:0x946b
# print('\u946b')                         #Unicode编码是16进制,输出Unicode码位(十六进制)
# print()

# #base64编码
# print('------------base64编码--------------')
# st = '喜学教育'                               #知识点，该字符为Unicode编码
# st_utf8_byte = st.encode('utf8')                 #Unicode编码转utf8编码byte格式
# st_utf8_base64 = base64.b64encode(st_utf8_byte)       #对byte格式base64编码，得到base64编码的byte格式
# print(st_utf8_base64.decode('utf8'))                    #utf8解码显示
# print()

# #base64解码
# print('------------base64解码--------------')
# base64_str='5Zac5a2m5pWZ6IKy'
# st_ = base64.b64decode(base64_str.encode())        #转化为byte格式，再进行base64解码，得到base64解码的byte格式
# print(st_.decode('utf8'))                           #utf8解码显示
# print()


# #图片编码base64
# with open('base64.jpg','rb') as f:
#     base64_data=base64.b64encode(f.read())
#     s = base64_data.decode('utf8')
#     print(s)

# #base64转图片
# byte = base64.b64decode(s.encode())
# with open('base64_2.jpg','wb') as f:
#     f.write(byte)
# print('--------------------------')




#补充：

# '''
# 字符串--->字节----->十六进制
# '''

# #第一种
# s='This'
# print(s.encode().hex())
# print(type(s.encode().hex()))    #字符串类型

# #第二种
# a=b'This'
# print(a.hex())
# print(type(a.hex()))            #字符串类型



# '''
# 总结：
# ord()用法:某一个字符的ascii码（type:int）
# >>> ord('a') 
# 97
# >>> type(ord('a'))
# <class 'int'>


# chr()用法：某一个int值的ascii符号(type:str)，
# >>> chr(97)
# 'a'
# >>> type(chr(97))
# <class 'str'>
# >>>

# hex()用法:其他进制---->十六进制，字节---->十六进制数(type:str)
# 例1：
# >>> hex(97) 
# '0x61'
# >>>

# 例2：
# >>> b'This'.hex()
# '54686973'
# >>> type(b'This'.hex()) 
# <class 'str'>
# >>>

# bin()用法:其他进制----->二进制，
# >>> bin(97) 
# '0b1100001'
# >>> type(bin(97)) 
# <class 'str'>

# '''


# '''
# 字符串--->十进制
# 首先要将字符串转为16进制，再转为十进制
# '''
# #方法一：
# ord('a')

# #方法二：
# s='This'
# print(int(s.encode().hex(),16))


# '''
# 十进制---->字符串
# '''
# chr(97)


#对字符串异或运算
def yara_xor(s=''):
    res1=''
    res2=''
    res3=''
    for i in s:
        r1=ord(i)^1
        r2=ord(i)^2
        r3=ord(i)^3
        res1+= chr(r1)
        res2+= chr(r2)
        res3+=chr(r3)
    print(res1)
    print(res2)
    print(res3)

if __name__ == '__main__':
    yara_xor('This program cannot')
