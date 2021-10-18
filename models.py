from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Seller(db.Model):
    __tablename__ = 'seller'
    id= db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    rut = db.Column(db.String(12), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    phonenumber = db.Column(db.String(15), nullable=False)
    storename = db.Column(db.String(30), nullable=False)   
    link = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    product = db.relationship("Product", backref=db.backref("seller", lazy = True))
    favorite = db.relationship("Favorite", backref=db.backref("seller", lazy = True))
    dispatch = db.relationship("Dispatch", backref=db.backref("seller", lazy = True))
    balance = db.relationship("Balance", backref=db.backref("seller", lazy = True))

    def __repr__(self):
        return "<Seller %r>" % self.id

    def serialize(self):
        return {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'rut': self.rut,
            'email': self.email,
            'password': self.password,
            'address': self.address,
            'phonenumber': self.phonenumber,
            'storename' : self.storename,           
            'link': self.link,
            'category': self.category
        }
    def serialize_just_name(self):
        return {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'storename': self.storename,
            'category': self.category
        }


class Buyer(db.Model):
    __tablename__ = 'buyer'
    id= db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    rut = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    favorite = db.relationship("Favorite", backref=db.backref("buyer", lazy = True))
    payment = db.relationship("Payment", backref=db.backref("buyer", lazy = True))

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
    productID = db.Column(db.Integer, db.ForeignKey('product.id'))
    item_title = db.Column(db.String(50), nullable= False) 
    item_price = db.Column(db.Integer, nullable= False)
    seller = db.relationship("Seller", backref=db.backref("seller", lazy = True))
    buyer = db.relationship("Buyer", backref=db.backref("buyer", lazy = True)) 
    product = db.relationship("Product", backref=db.backref("product", lazy = True))
     

    def __repr__(self):
        return "<Sale %r>" % self.id

    def serialize(self):
        return {
            'id': self.id,
            'sellerID': self.sellerID,
            'buyerID': self.buyerID,
            'productID': self.productID,
            'item_title': self.item_title,
            'item_price': self.item_price
        }
    def serialize_just_name(self):
        return {
            'id': self.id,
            'sellerID': self.sellerID
        }


class Product(db.Model):
    __tablename__= 'product'
    id= db.Column(db.Integer, primary_key=True)
    sellerID = db.Column(db.Integer, db.ForeignKey('seller.id'))
    storename = db.Column(db.String(30), nullable=False)
    item_title = db.Column(db.String(50), nullable=False)
    item_photo = db.Column(db.String(250), nullable=False)
    item_description = db.Column(db.String(250), nullable=False)
    item_stock = db.Column(db.Integer, nullable=False)
    item_price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<Product %r>" % self.id

    def serialize(self):
        return {
            'id': self.id,
            'sellerID': self.sellerID,
            'storename': self.storename,
            'item_title': self.item_title,
            'item_photo': self.item_photo,
            'item_description': self.item_description,
            'item_stock': self.item_stock,
            'item_price': self.item_price
        }

    def serialize_just_name(self):
        return {
            'id': self.id,
            'sellerID': self.sellerID,
            'storename': self.storename,
            'item_title': self.item_title
        }


class Favorite(db.Model):
    __tablename__= 'favorite'
    id = db.Column(db.Integer, primary_key=True)
    buyerID = db.Column(db.Integer, db.ForeignKey('buyer.id'))
    sellerID = db.Column(db.Integer, db.ForeignKey('seller.id'))
    storename = db.Column(db.String(30), nullable=False)
    
    

    def __repr__(self):
        return "<Favorite %r>" % self.id

    def serialize(self):
        return {
            'id': self.id,
            'buyerID': self.buyerID,
            'sellerID': self.sellerID,
            'storename': self.storename
        }
    
    def serialize_just_name(self):
        return {
            'id': self.id,
            'storename': self.storename
        }


class Payment(db.Model):
    __tablename__= 'payment'
    id= db.Column(db.Integer, primary_key=True)
    buyerID = db.Column(db.Integer, db.ForeignKey('buyer.id'))
    debit = db.Column(db.Boolean, default=False, nullable=False)
    credit = db.Column(db.Boolean, default=False, nullable=False)
    transfer = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return "<Payment %r>" % self.id

    def serialize(self):
        return {
            'id': self.id,
            'buyerID': self.buyerID,
            'debit': self.debit,
            'credit': self.credit,
            'transfer': self.transfer
        }

    def serialize_just_name(self):
        return {
            'id': self.id,
            'debit': self.debit,
            'credit': self.credit,
            'transfer': self.transfer
        }


class Dispatch(db.Model):
    __tablename__= 'dispatch'
    id= db.Column(db.Integer, primary_key=True)
    sellerID = db.Column(db.Integer, db.ForeignKey('seller.id'))
    in_address = db.Column(db.String(100), nullable=False)
    delivery = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return "<Dispatch %r>" % self.id

    def serialize(self):
        return {
            'id': self.id,
            'sellerID': self.sellerID,
            'in_address': self.in_address,
            'delivery': self.delivery
        }

    def serialize_just_name(self):
        return {
            'id': self.id,
            'in_address': self.in_address,
            'delivery': self.delivery
        }


class Balance(db.Model):
    __tablename__= 'balance'
    id= db.Column(db.Integer, primary_key=True)
    sellerID = db.Column(db.Integer, db.ForeignKey('seller.id'))
    storename = db.Column(db.String(30), nullable=False)
    current_balance = db.Column(db.Integer, nullable=False)
    last_deposit = db.Column(db.Integer, nullable=False)
    last_withdraw = db.Column(db.Integer, nullable=False)
    

    def __repr__(self):
        return "<Balance %r>" % self.id

    def serialize(self):
        return {
            'id': self.id,
            'sellerID': self.sellerID,
            'storename': self.storename,
            'current_balance': self.current_balance,
            'last_deposit': self.last_deposit,
            'last_withdraw': self.last_withdraw
        }

    def serialize_just_name(self):
        return {
            'id': self.id,
            'storename': self.storename,
            'current_balance': self.current_balance,
            'last_deposit': self.last_deposit,
            'last_withdraw': self.last_withdraw
        }