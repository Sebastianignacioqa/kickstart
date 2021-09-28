from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from models import db, Seller, Buyer
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:isac1234@localhost:5432/blog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
db.init_app(app)
Migrate(app, db)

@app.route ("/seller", methods=["GET", "POST"])
def seller():
    if request.method == "GET":
        seller = Seller.query.get(1)
        return jsonify(user.serialize()), 200
    else:
        seller = Seller()
        seller.firstname = request.json.get("firstname")
        seller.lastname = request.json.get("lastname")
        seller.rut = request.json.get("rut")
        seller.password = request.json.get("password")
        seller.email = request.json.get("email")
        seller.link = request.json.get("link")
        

        db.session.add(seller)
        db.session.commit()

    return jsonify(user.serialize()), 200

@app.route ("/buyer", methods=["GET", "POST"])
def buyerr():
    if request.method == "GET":
        buyer = Buyer.query.get(1)
        return jsonify(user.serialize()), 200
    else:
        buyer = Buyer()
        buyer.firstname = request.json.get("firstname")
        buyer.lastname = request.json.get("lastname")
        buyer.rut = request.json.get("rut")
        buyer.password = request.json.get("password")
        buyer.email = request.json.get("email")
        
        

        db.session.add(buyer)
        db.session.commit()

    return jsonify(user.serialize()), 200


if __name__== "__main__":
    app.run(host='localhost', port = 8080)
