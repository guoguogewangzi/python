from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

# 连接到SQLite数据库
conn = sqlite3.connect('users.db',check_same_thread=False)
c = conn.cursor()

# 创建用户表
# c.execute('''CREATE TABLE IF NOT EXISTS users
#              (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''')
# conn.commit()

# 获取所有用户
@app.route('/users', methods=['GET'])
def get_users():
    c.execute('SELECT * FROM users')
    users = c.fetchall()
    return jsonify(users)

# 获取单个用户
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    c.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = c.fetchone()
    if user:
        return jsonify(user)
    else:
        return jsonify({"error": "User not found"}), 404

# 创建新用户
@app.route('/users', methods=['POST'])
def create_user():
    new_user = {
        "name": request.json.get('name'),
        "age": request.json.get('age')
    }
    c.execute('INSERT INTO users (name, age) VALUES (?, ?)', (new_user['name'], new_user['age']))
    conn.commit()
    new_user['id'] = c.lastrowid
    return jsonify(new_user), 201

# 更新用户信息
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    updated_user = {
        "name": request.json.get('name'),
        "age": request.json.get('age')
    }
    c.execute('UPDATE users SET name = ?, age = ? WHERE id = ?', (updated_user['name'], updated_user['age'], user_id))
    conn.commit()
    if c.rowcount > 0:
        return jsonify(updated_user)
    else:
        return jsonify({"error": "User not found"}), 404

# 删除用户
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    c.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    if c.rowcount > 0:
        return jsonify({"message": "User deleted"})
    else:
        return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    app.run()
    
    
    



'''
1.‘查询’数据的数据包
----------------------
GET /users HTTP/1.1
Host: 127.0.0.1:5000
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate, br
Connection: close
----------------------
'''

'''
2.‘查询单个用户’数据的数据包
----------------------
GET /users/1 HTTP/1.1
Host: 127.0.0.1:5000
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate, br
Connection: close
Upgrade-Insecure-Requests: 1
----------------------

'''

'''
3.‘插入’数据的数据包
----------------------
POST /users HTTP/1.1
Host: 127.0.0.1:5000
User-Agent: python-requests/2.25.1
Accept-Encoding: gzip, deflate, br
Accept: */*
Connection: close
Content-Length: 31
Content-Type: application/json

{"name": "John Doe", "age": 25}
----------------------
'''

'''
4.‘更新’数据的数据包
----------------------
PUT /users/1 HTTP/1.1
Host: 127.0.0.1:5000
User-Agent: python-requests/2.25.1
Accept-Encoding: gzip, deflate, br
Accept: */*
Connection: close
Content-Length: 31
Content-Type: application/json

{"name": "John Doe", "age": 25}
----------------------
'''

'''
5.‘删除’数据的数据包
----------------------
DELETE /users/6	 HTTP/1.1
Host: 127.0.0.1:5000
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate, br
Connection: close
----------------------
'''