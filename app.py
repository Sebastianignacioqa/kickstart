from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from models import db, Seller, Buyer, Sale, Product
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:isac1234@localhost:5432/kickstart'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
app.config["JWT_SECRET_KEY"] = "super-secret"

db.init_app(app)
Migrate(app, db)
CORS(app)
jwt = JWTManager(app)

@app.route ("/seller", methods=["GET", "POST"])
def seller():
    if request.method == "GET":
        seller = Seller.query.get(1)
        return jsonify(seller.serialize()), 200
    else:
        seller = Seller()
        seller.firstname = request.json.get("firstname")
        seller.lastname = request.json.get("lastname")
        seller.rut = request.json.get("rut")
        seller.store_name = request.json.get("store_name")
        seller.password = request.json.get("password")
        seller.email = request.json.get("email")
        seller.link = request.json.get("link")
        

        db.session.add(seller)
        db.session.commit()

    return jsonify(seller.serialize()), 200

@app.route ("/buyer", methods=["GET", "POST"])
def buyer():
    if request.method == "GET":
        buyer = Buyer.query.get(1)
        return jsonify(buyer.serialize()), 200
    else:
        buyer = Buyer()
        buyer.firstname = request.json.get("firstname")
        buyer.lastname = request.json.get("lastname")
        buyer.rut = request.json.get("rut")
        buyer.password = request.json.get("password")
        buyer.email = request.json.get("email")
        
        

        db.session.add(buyer)
        db.session.commit()

    return jsonify(buyer.serialize()), 200

@app.route ("/sale", methods=["GET", "POST"])
def sale():
    if request.method == "GET":
        sale = Sale.query.get(1)
        return jsonify(sale.serialize()), 200
    else:
        sale = Sale()
        sale.sellerID = request.json.get("sellerID")
        sale.buyerID = request.json.get("buyerID")

        

        db.session.add(sale)
        db.session.commit()

    return jsonify(sale.serialize()), 200

@app.route ("/product", methods=["GET", "POST"])
def product():
    if request.method == "GET":
        product = Product.query.get(1)
        return jsonify(product.serialize()), 200
    else:
        product = Product()
        product.sellerID = request.json.get("sellerID")
        product.store_name = request.json.get("store_name")
        product.item_title = request.json.get("item_title")
        product.item_photo = request.json.get("item_photo")
        product.item_description = request.json.get("item_description")
        product.item_stock = request.json.get("item_stock")
        product.item_price = request.json.get("item_price")

        

        db.session.add(product)
        db.session.commit()

    return jsonify(product.serialize()), 200

@app.route ("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        seller = Seller.query.get(1)
        return jsonify(seller.serialize()), 200
    else:
        seller = Seller()
        seller.rut = request.json.get("rut")
        seller.password = request.json.get("password")

    return jsonify(seller.serialize_just_login()), 200
    

@app.route ("/login2", methods=["GET", "POST"])
def login2():
    if request.method == "GET":
        buyer = Buyer.query.get(1)
        return jsonify(buyer.serialize()), 200
    else:
        buyer = Buyer()
        buyer.rut = request.json.get("rut")
        buyer.password = request.json.get("password")

    return jsonify(buyer.serialize_just_login()), 200


if __name__== "__main__":
    app.run(host='localhost', port = 8080)
