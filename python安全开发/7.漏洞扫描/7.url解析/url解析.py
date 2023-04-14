from urllib import parse

# url = 'http://192.168.1.100/admin/login.php'
url = 'http://192.168.1.100:8080/admin/login.php'

result = parse.urlparse(url)
print(result)
#ParseResult(scheme='http', netloc='192.168.1.100:8080', path='/admin/login.php', params='', query='', fragment='')


host = result.netloc   #取netloc值

host = host.split(':')[0]

print(host)
