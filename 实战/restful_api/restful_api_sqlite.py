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