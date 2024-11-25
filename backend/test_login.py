import pytest
from flask import Flask, request
from flask_jwt_extended import JWTManager,create_access_token
from werkzeug.security import check_password_hash, generate_password_hash
from flask import jsonify
import json

# 假设这里有简单的用户数据存储方式，实际应用中应从数据库获取用户数据
users = [
    {"username": "user", "password": generate_password_hash("123456")},
    {"username": "user2", "password": generate_password_hash("pass2")}
]

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "your-secret-key"
    jwt_manager = JWTManager(app)

    @app.route('/login', methods=['POST'])
    def login():
        # 从flask框架引入request对象以获取POST请求的JSON数据
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        for user in users:
            if user['username'] == username and check_password_hash(user['password'], password):
                access_token = create_access_token(identity=username)
                return jsonify({"success": True, "access_token": access_token})
        return jsonify({"success": False})

    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_login_success(client):
    # 模拟正确的登录请求
    data = {
        "username": "user",
        "password": "123456"
    }
    response = client.post('/login', json=data)
    assert response.status_code == 200
    assert response.json["success"] == True

def test_login_failure(client):
    # 模拟错误的登录请求
    data = {
        "username": "user1",
        "password": "wrong_password"
    }
    response = client.post('/login', json=data)
    assert response.status_code == 200
    assert response.json["success"] == False