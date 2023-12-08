from flask import Flask, jsonify, request

app = Flask(__name__)

# 模拟一个简单的数据存储
users = [
    {"id": 1, "name": "Alice", "age": 25},
    {"id": 2, "name": "Bob", "age": 30},
    {"id": 3, "name": "Charlie", "age": 35}
]

# 获取所有用户
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

# 获取单个用户
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((user for user in users if user['id'] == user_id), None)
    if user:
        return jsonify(user)
    else:
        return jsonify({"error": "User not found"}), 404

# 创建新用户
@app.route('/users', methods=['POST'])
def create_user():
    new_user = {
        "id": request.json.get('id'),
        "name": request.json.get('name'),
        "age": request.json.get('age')
    }
    users.append(new_user)
    return jsonify(new_user), 201

# 更新用户信息
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = next((user for user in users if user['id'] == user_id), None)
    if user:
        user['name'] = request.json.get('name', user['name'])
        user['age'] = request.json.get('age', user['age'])
        return jsonify(user)
    else:
        return jsonify({"error": "User not found"}), 404

# 删除用户
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = next((user for user in users if user['id'] == user_id), None)
    if user:
        users.remove(user)
        return jsonify({"message": "User deleted"})
    else:
        return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    app.run()