import pymysql

#连接数据库
conn=pymysql.connect(host='localhost',user='root',passwd='root')

#创建游标对象
cursor=conn.cursor()

cursor.execute('show databases')
result =cursor.fetchall()
print(result)
cursor.execute('use test')
cursor.execute('show tables')
result =cursor.fetchall()
print(result)
cursor.execute('select * from student')
result =cursor.fetchall()
print(result)
for line in result:
    print(line)





