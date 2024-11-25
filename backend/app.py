from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from models import User, Product, Contact, db, generate_random_data

app = Flask(__name__)
CORS(app)



app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portal.db'
app.config['JWT_SECRET_KEY'] = 'your-secret-key'
jwt = JWTManager(app)
db.init_app(app)

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if 'user'== data['username'] and '123456' == data['password']:
        access_token = create_access_token(identity=data['username'])
        return jsonify({"token": access_token}), 200
    return jsonify({"msg": "Invalid credentials"}), 401

@app.route('/api/logout', methods=['POST'])
@jwt_required()
def logout():
    return jsonify({"msg": "Successfully logged out"}), 200

@app.route('/api/products')
def get_products():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = 10  # 每页显示的产品数量，可根据需求修改

        # 查询产品数据并进行分页
        products_query = Product.query.order_by(Product.id)
        products = products_query.paginate(page=page, per_page=per_page, error_out=False)

        product_list = []
        for product in products.items:
            product_dict = {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": product.price
            }
            product_list.append(product_dict)

        return jsonify({
            "products": product_list,
            "total": products.total
        }), 200
    except Exception as e:
        print(f"获取产品数据时出错: {e}")
        return jsonify({"error": "获取产品数据失败，请稍后再试。"}), 500

@app.route('/api/contact', methods=['POST'])
def submit_contact():
    data = request.get_json()
    contact = Contact(
        name=data['name'],
        email=data['email'],
        message=data['message']
    )
    db.session.add(contact)
    db.session.commit()
    return jsonify({"msg": "Contact submitted successfully"}), 201

@app.route('/')
@jwt_required()
def home():
    return "Welcome to the home page!"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        generate_random_data()
        # db.create_all()
    app.run(debug=True)
