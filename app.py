from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models import db, Seller, Buyer, Sale, Product
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask_wtf import Form
from wtforms import StringField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, Email
import os
from flask_bcrypt import Bcrypt
import re
from datetime import datetime

UPLOAD_FOLDER = 'documents'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:isac1234@localhost:5432/kickstart'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
app.config["JWT_SECRET_KEY"] = "super-secret"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["SECRET_KEY"] = "other-super-secret"



db.init_app(app)
Migrate(app, db)
CORS(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

class DocumentUploadForm(Form):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    document = FileField("Document", validators=[FileRequired(), FileAllowed(['png', 'jpg', 'jpeg', 'gif'], 'IMAGE ONLY')])


@app.route ("/seller", methods=["GET", "POST"])
def seller():
    if request.method == "GET":
        seller = Seller.query.get(1)
        return jsonify(seller.serialize()), 200
    else:
        seller = Seller()
        firstname = request.json.get("firstname")
        lastname = request.json.get("lastname")
        rut = request.json.get("rut")
        store_name = request.json.get("store_name")
        password = request.json.get("password")
        email = request.json.get("email")
        link = request.json.get("link")

        seller= Seller.query.filter_by(rut=rut).first()
        if seller is None:
            seller = Seller()
            seller.firstname = firstname
            seller.lastname = lastname
            #Validating rut
            rut_regex = '^(\d{2}\\d{3}\\d{3}-)([a-zA-Z]{1}$|\d{1}$)'
            if re.search(rut_regex, rut):
                seller.rut = rut
            else:
                return jsonify({
                    "msg": "El RUT no es valido"
                }), 400
            seller.store_name = store_name
            #validating password
            password_regex = '^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$'
            if re.search(password_regex, password):
                password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
                seller.password = password_hash
            else:
                return jsonify({
                    "msg": "El password no es valido"
                }), 400
            seller.email = email
            seller.link = link

            db.session.add(seller)
            db.session.commit()

            return jsonify({
                "msg": "Vendedor registrado corectamente"
            }),200
        else:
            return jsonify({
                "msg": "El vendedor ya se encuentra registrado"
            }),400

@app.route ("/buyer", methods=["GET", "POST"])
def buyer():
    if request.method == "GET":
        buyer = Buyer.query.get(1)
        return jsonify(buyer.serialize()), 200
    else:
        buyer = Buyer()
        firstname = request.json.get("firstname")
        lastname = request.json.get("lastname")
        rut = request.json.get("rut")
        password = request.json.get("password")
        email = request.json.get("email")

        buyer= Buyer.query.filter_by(rut=rut).first()
        if buyer is None:
            buyer = Buyer()
            buyer.firstname = firstname
            buyer.lastname = lastname
            #Validating rut
            rut_regex = '^(\d{2}\\d{3}\\d{3}-)([a-zA-Z]{1}$|\d{1}$)'
            if re.search(rut_regex, rut):
                buyer.rut = rut
            else:
                return jsonify({
                    "msg": "El RUT no es valido"
                }), 400
            #validating password
            password_regex = '^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$'
            if re.search(password_regex, password):
                password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
                buyer.password = password_hash
            else:
                return jsonify({
                    "msg": "El password no es valido"
                }), 400
            buyer.email = email

            db.session.add(buyer)
            db.session.commit()

            return jsonify({
                "msg": "Comprador registrado corectamente"
            }),200
        else:
            return jsonify({
                "msg": "El Comprador ya se encuentra registrado"
            }),400

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
        product.item_title = request.json.get("item_title")
        product.file = request.json.get("file")
        product.item_description = request.json.get("item_description")
        product.item_stock = request.json.get("item_stock")
        product.item_price = request.json.get("item_price")
        product.category = request.json.get("category")

        

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
        rut = request.json.get("rut")
        password = request.json.get("password")

        if password == "":
            return jsonify({
                "msg": "Debes ingresar un password valido"
            }), 400
        if rut == "":
            return jsonify({
                "msg": "Debes ingresar un RUT valido"
            }), 400   

        seller = Seller.query.filter_by(rut=rut).first()

        if seller is None:
           return jsonify({
                "msg": "Este vendedor no existe, debes registrarte"
            }), 400
        elif bcrypt.check_password_hash(seller.password, password):
            access_token = create_access_token(identity=seller.rut)
            return jsonify({
                "msg": "User login success",
                "access_token": access_token,
                "seller": seller.serialize_just_login()
            }), 200
        else:
            return jsonify({
                "msg": "Credenciales erroneas"
            }), 400



@app.route ("/log", methods=["POST"])
@jwt_required()
def log(): 
    current_user = get_jwt_identity()
    current_user_token_expires = get_jwt()["exp"]
    return jsonify({
        "current_user" : current_user,
        "current_user_token_expires": datetime.fromtimecodstamp(current_user_token_expires)
    }),200


    

@app.route ("/login2", methods=["GET", "POST"])
def login2():
    if request.method == "GET":
        buyer = Buyer.query.get(1)
        return jsonify(buyer.serialize()), 200
    else:
        buyer = Buyer()
        rut = request.json.get("rut")
        password = request.json.get("password")

        if password == "":
            return jsonify({
                "msg": "Debes ingresar un password valido"
            }), 400
        if rut == "":
            return jsonify({
                "msg": "Debes ingresar un RUT valido"
            }), 400   

        buyer = Buyer.query.filter_by(rut=rut).first()

        if buyer is None:
           return jsonify({
                "msg": "Este comprador no existe, debes registrarte"
            }), 400
        elif bcrypt.check_password_hash(buyer.password, password):
            access_token = create_access_token(identity=buyer.rut)
            return jsonify({
                "msg": "User login success",
                "access_token": access_token,
                "buyer": buyer.serialize_just_login()
            }), 200
        else:
            return jsonify({
                "msg": "Credenciales erroneas"
            }), 400

if __name__== "__main__":
    app.run(host='localhost', port = 8080)
