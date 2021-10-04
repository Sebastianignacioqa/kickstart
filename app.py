from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from models import db, Seller, Buyer, Sales, Postseller, Favorites
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/kickstart'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
db.init_app(app)
Migrate(app, db)

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

@app.route ("/sales", methods=["GET", "POST"])
def sales():
    if request.method == "GET":
        sales = Sales.query.get(1)
        return jsonify(sales.serialize()), 200
    else:
        sales = Sales()
        sales.seller = request.json.get("sales")
        sales.buyer = request.json.get("buyer")

        

        db.session.add(sales)
        db.session.commit()

    return jsonify(sales.serialize()), 200


@app.route ("/postseller", methods=["GET", "POST", "PUT"])
def postseller():
    if request.method == "GET":
        postseller = Postseller.query.get(1)
        return jsonify(postseller.serialize()), 200
        
    if request.method == "PUT":
        postseller = Postseller.query.get(1)
        postseller.item_title = ""
        postseller.item_photo = ""
        postseller.item_description = ""
        postseller.item_stock = ""
        postseller.item_price = ""

        db.session.commit()
    else:
        postseller = Postseller()
        postseller.store_name = request.json.get("store_name")
        postseller.item_title = request.json.get("item_title")
        postseller.item_photo = request.json.get("item_photo")
        postseller.item_description = request.json.get("item_description")
        postseller.item_stock = request.json.get("item_stock")
        postseller.item_price = request.json.get("item_price")

        db.session.add(postseller)
        db.session.commit()

    return jsonify(postseller.serialize()), 200


@app.route ("/favorites", methods=["GET", "POST"])
def favorites():
    if request.method == "GET":
        favorites = Favorites.query.get(1)
        return jsonify(favorites.serialize()), 200
    else:
        favorites = Favorites()
        favorites.store_name = request.json.get("store_name")    

        db.session.add(favorites)
        db.session.commit()

    return jsonify(favorites.serialize()), 200


if __name__== "__main__":
    app.run(host='localhost', port = 8080)
