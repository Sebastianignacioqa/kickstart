from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Seller(db.Model):
    __tablename__ = 'seller'
    id= db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    rut = db.Column(db.String(10), nullable=False)
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
            'password': self.password,
            'email': self.email,
            'link': self.link
        }
    def serialize_just_name(self):
        return {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname
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

class Sales(db.Model):
    __tablename__ = 'sales'
    id= db.Column(db.Integer, primary_key=True)
    seller = db.Column(db.String(50), nullable=False)
    buyer = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return "<Post %r>" % self.id

    def serialize(self):
        return {
            'id': self.id,
            'seller': self.seller,
            'buyer': self.buyer,
            'amount': self.amount
        }
    def serialize_just_name(self):
        return {
            'id': self.id,
            'selles': self.firstname,
            'amount': self.amount
        }