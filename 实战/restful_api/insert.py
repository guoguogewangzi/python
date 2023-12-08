import requests

# 要插入的数据
new_user = {
    "name": "John Doe",
    "age": 25
}

proxies = {"http":"http://127.0.0.1:8080","https":"http://127.0.0.1:8080"}
# 发送POST请求
response = requests.post('http://127.0.0.1:5000/users', json=new_user,proxies=proxies)

# 检查响应状态码
if response.status_code == 201:
    print("数据插入成功")
else:
    print("数据插入失败")