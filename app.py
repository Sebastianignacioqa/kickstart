from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models import db, Seller, Buyer, Sale, Product, Images, Favorite, Category, Balance, Payment, Dispatch, Wishlist
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
import mercadopago
from flask import send_from_directory

UPLOAD_FOLDER = 'documents'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:6kjqxSDJ44!w@localhost:5432/kickstart'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
app.config["JWT_SECRET_KEY"] = "super-secret"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_PATH'] = 'documents'
app.config["SECRET_KEY"] = "other-super-secret"
sdk=mercadopago.SDK("TEST-92550965623394-111201-15d34088f585edbda78b8842d42cfa0d-439478684")


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


@app.route ("/registrocomprador", methods=["GET", "POST"])
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

#@app.route ("/pago", methods=["POST"])
#def payment():
 #  preference_data = {
#    "items": [
#    {
 #   "title": request.json.get("item_title"),
#   #"quantity": item_stock ,
 #   "unit_price": request.json.get("item_price") 
 #   }
 #   ]
 #   }
    
 #   preference_response = sdk.preference().create(preference_data)
 #   preference = preference_response["response"]

 #   db.session.add(payment)
 #   db.session.commit()

 #   return jsonify(payment.serialize()), 200



@app.route ("/product", methods=["GET", "POST"])
def product():
    if request.method == "GET":
        _product = Product.query.all()
        products_list = [_product.serialize_just_sell() for _product in _product]
        return jsonify(products_list), 200

    else:
        product = Product()
        product.item_title = request.json.get("item_title")
        product.item_description = request.json.get("item_description")
        product.item_stock = request.json.get("item_stock")
        product.item_price = request.json.get("item_price")
        product.category_id = request.json.get("category_id")
        product.sellerID = request.json.get("sellerID")
    
        db.session.add(product)
        db.session.commit()

        return jsonify({"msg": "Ok"}),200

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
            }), 401
        elif bcrypt.check_password_hash(seller.password, password):
            access_token = create_access_token(identity=seller.rut)
            return jsonify({
                "msg": "User login success",
                "access_token": access_token,
                "seller": seller.serialize_just_id()
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
        "current_user_token_expires": datetime.fromtimestamp(current_user_token_expires)
    }),200

@app.route ("/wishlist", methods=["GET", "POST"])
def wishlist():
    if request.method == "GET":
        _wishlist = Wishlist.query.all()
        wishlist_list = [_wishlist.serialize() for _wishlist in _wishlist]
        return jsonify(wishlist_list), 200

    else:
        wishlist = Wishlist()
        wishlist.sellerID = request.json.get("sellerID")
    
        db.session.add(wishlist)
        db.session.commit()

        return jsonify({"msg": "Ok"}),200

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
            }), 401
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
                "buyer": buyer.serialize_just_id()
            }), 200
        else:
            return jsonify({
                "msg": "Credenciales erroneas"
            }), 400

@app.route('/post', methods=['POST'])
def upload_files():
    for uploaded_file in request.files.getlist('file'):
        if uploaded_file.filename != '':
            uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename))
            
    return "El documento fue adjunto satisfactoriamente"

@app.route ("/categories", methods=["POST", "GET"])
def categories():
    if request.method == "POST":
        category = Category()
        category.name = request.json.get("name")
        category_exist = Category.query.filter_by(name=request.json.get("name")).first()
        if category_exist is not None:
            return jsonify("Categoría ya existe"), 400

        db.session.add(category)
        db.session.commit()

        return jsonify("Categoría creada"), 200

    else:
        _category = Category.query.all()
        categories_list = [_category.serialize() for _category in _category]
        return jsonify(categories_list), 200


@app.route ("/categorias", methods=["GET", "POST"])
def categorias():
    if request.method == "POST":
        categoria = request.json.get("categoria")
        if categoria is None:
            return jsonify("Categoría no válida"), 400
        else:
            arreglo=[]
            categorias = Seller.query.filter_by(category_id=categoria).all()
            if categorias is None:
                return jsonify("No existen tiendas"), 200
            for category_id in categorias:
                arreglo.append(category_id.storename)
            return jsonify(arreglo), 200

@app.route ("/registrotienda", methods=["GET", "POST"])
def seller():
    if request.method == "GET":
        seller = Seller.query.get(1)
        return jsonify(seller.serialize()), 200
    else:
        firstname = request.json.get("firstname")
        lastname = request.json.get("lastname")
        rut = request.json.get("rut")
        email = request.json.get("email")
        password = request.json.get("password")
        address = request.json.get("address")
        phonenumber = request.json.get("phonenumber")
        storename = request.json.get("storename")       
        link = request.json.get("link")
        category_id = request.json.get("category_id")

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
            seller.storename = storename
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
            seller.address = address
            seller.phonenumber = phonenumber
            seller.category_id = category_id

            db.session.add(seller)
            db.session.commit()

            return jsonify({
                "msg": "Vendedor registrado corectamente"
            }),200
        else:
            return jsonify({
                "msg": "El vendedor ya se encuentra registrado"
            }),400

        return jsonify(seller.serialize()), 200


@app.route ("/favorite", methods=["GET", "POST"])
def favorite():
    if request.method == "GET":
        favorite = Favorite.query.get(1)
        return jsonify(favorite.serialize()), 200
    else:
        favorite = Favorite()
        favorite.buyerID = request.json.get("buyerID")
        favorite.sellerID = request.json.get("sellerID")
        favorite.storename = request.json.get("storename")    

        db.session.add(favorite)
        db.session.commit()

        return jsonify(favorite.serialize()), 200

#@app.route ("/payment", methods=["GET", "POST"])
#def payment():
#    if request.method == "GET":
#        payment = Payment.query.get(1)
#       return jsonify(payment.serialize()), 200
#    else:
#        payment = Payment()
#        payment.buyerID = request.json.get("buyerID")
#        payment.debit = request.json.get("debit")
#        payment.credit = request.json.get("credit")
#        payment.transfer = request.json.get("transfer")     

        #db.session.add(payment)
        #db.session.commit()

        #return jsonify(payment.serialize()), 200

@app.route ("/dispatch", methods=["GET", "POST"])
def dispatch():
    if request.method == "GET":
        dispatch = Dispatch.query.get(1)
        return jsonify(dispatch.serialize()), 200
    else:
        dispatch = Dispatch()
        dispatch.sellerID = request.json.get("sellerID")
        dispatch.in_address = request.json.get("in_address")
        dispatch.delivery = request.json.get("delivery")   

        db.session.add(dispatch)
        db.session.commit()

        return jsonify(dispatch.serialize()), 200

@app.route ("/balance", methods=["GET", "POST"])
def balance():
    if request.method == "GET":
        balance = Balance.query.get(1)
        return jsonify(balance.serialize()), 200
    else:
        balance = Balance()
        balance.sellerID = request.json.get("sellerID")
        balance.storename = request.json.get("storename")
        balance.current_balance = request.json.get("current_balance")
        balance.last_deposit = request.json.get("last_deposit")
        balance.last_withdraw = request.json.get("last_withdraw")        

        db.session.add(balance)
        db.session.commit()

        return jsonify(balance.serialize()), 200


if __name__== "__main__":
    app.run(host='localhost', port = 8080)