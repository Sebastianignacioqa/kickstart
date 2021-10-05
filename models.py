from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Seller(db.Model):
    __tablename__ = 'seller'
    id= db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    rut = db.Column(db.Integer, nullable=False)
    store_name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    link = db.Column(db.String(100), nullable=False)
    

    def __repr__(self):
        return "<Seller %r>" % self.id

    def serialize(self):
        return {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'rut': self.rut,
            'store_name' : self.store_name,
            'password': self.password,
            'email': self.email,
            'link': self.link
        }
    def serialize_just_name(self):
        return {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'store_name' : self.store_name
        }

class Buyer(db.Model):
    __tablename__ = 'buyer'
    id= db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    rut = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return "<Post %r>" % self.id

    def serialize(self):
        return {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'rut': self.rut,
            'password': self.password,
            'email': self.email
        }
    def serialize_just_name(self):
        return {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname
        }

class Sale(db.Model):
    __tablename__ = 'sale'
    id= db.Column(db.Integer, primary_key=True)
    sellerID = db.Column(db.Integer, db.ForeignKey('seller.id'))
    buyerID = db.Column(db.Integer, db.ForeignKey('buyer.id'))
    seller = db.relationship("Seller", backref=db.backref("seller", lazy = True))
    buyer = db.relationship("Buyer", backref=db.backref("buyer", lazy = True))
   # postID = Column(Integer, nullable= False) FALTA TABA POST
   # item_title = Column(Integer, nullable= False) FALTA TABLA POST
    #item_price =Column(Integer, nullable= False) FALTA TABLA POST

    def __repr__(self):
        return "<Post %r>" % self.id

    def serialize(self):
        return {
            'id': self.id,
            'seller': self.seller,
            'buyer': self.buyer,
            #'postID': self.postID FALTA TABA POST
            #'item_title': self.item_title FALTA TABA POST
            #'item_price': self.item_price FALTA TABA POST
        }
    def serialize_just_name(self):
        return {
            'id': self.id,
            'seller': self.seller,
            
        }


class Product(db.Model):
    __tablename__= 'product'
    id= db.Column(db.Integer, primary_key=True)
    store_name = db.Column(db.String(30), nullable=False)
    item_title = db.Column(db.String(50), nullable=False)
    item_photo = db.Column(db.String(250), nullable=False)
    item_description = db.Column(db.String(150), nullable=False)
    item_stock = db.Column(db.String(15), nullable=False)
    item_price = db.Column(db.Integer, nullable=False)
    sellerID

    def __repr__(self):
        return "<Product %r>" % self.id

    def serialize(self):
        return {
            'id': self.id,
            'store_name': self.store_name,
            'item_title': self.item_title,
            'item_photo': self.item_photo,
            'item_description': self.item_description,
            'item_stock': self.item_stock,
            'item_price': self.item_price
        }
    def serialize_just_name(self):
        return {
            'id': self.id,
            'store_name': self.store_name,
            'item_title': self.item_title
        }

class Favorite(db.Model):
    __tablename__= 'favorite'
    id= db.Column(db.Integer, primary_key=True)
    store_name = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return "<Favorite %r>" % self.id

    def serialize(self):
        return {
            'id': self.id,
            'store_name': self.store_name
        }