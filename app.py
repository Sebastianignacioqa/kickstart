from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from models import db, Seller, Buyer, Sale, Product, Favorite, Payment, Dispatch, Balance, Category
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/kickstart3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
db.init_app(app)
Migrate(app, db)
CORS(app)

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
            categorias = Seller.query.filter_by(category=categoria).all()
            if categorias is None:
                return jsonify("No existen tiendas"), 200
            for category in categorias:
                arreglo.append(category.storename)
            return jsonify(arreglo), 200
            

@app.route ("/registrotienda", methods=["GET", "POST"])
def seller():
    if request.method == "GET":
        seller = Seller.query.get(1)
        return jsonify(seller.serialize()), 200
    else:
        seller = Seller()
        seller.firstname = request.json.get("firstname")
        seller.lastname = request.json.get("lastname")
        seller.rut = request.json.get("rut")
        seller.email = request.json.get("email")
        seller.password = request.json.get("password")
        seller.address = request.json.get("address")
        seller.phonenumber = request.json.get("phonenumber")
        seller.storename = request.json.get("storename")       
        seller.link = request.json.get("link")
        seller.category_id = request.json.get("category_id")

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


@app.route ("/product", methods=["GET", "POST", "PUT"])
def product():
    if request.method == "GET":
        product = Product.query.get(1)
        return jsonify(product.serialize()), 200
        
    if request.method == "PUT":
        product = Product.query.get(1)
        product.item_title = ""
        product.item_photo = ""
        product.item_description = ""
        product.item_stock = ""
        product.item_price = ""

        db.session.commit()
    else:
        product = Product()
        product.sellerID = request.json.get("sellerID")
        product.storename = request.json.get("storename")
        product.item_title = request.json.get("item_title")
        product.item_photo = request.json.get("item_photo")
        product.item_description = request.json.get("item_description")
        product.item_stock = request.json.get("item_stock")
        product.item_price = request.json.get("item_price")

        db.session.add(product)
        db.session.commit()

        return jsonify(product.serialize()), 200


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

@app.route ("/payment", methods=["GET", "POST"])
def payment():
    if request.method == "GET":
        payment = Payment.query.get(1)
        return jsonify(payment.serialize()), 200
    else:
        payment = Payment()
        payment.buyerID = request.json.get("buyerID")
        payment.debit = request.json.get("debit")
        payment.credit = request.json.get("credit")
        payment.transfer = request.json.get("transfer")     

        db.session.add(payment)
        db.session.commit()

        return jsonify(payment.serialize()), 200

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
