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



class Balance(db.Model):
    __tablename__ = 'balance'
    id= db.Column(db.Integer, primary_key=True)
    current_balance = db.Column(db.Integer)
    last_deposit = db.Column(db.Integer)
    last_withdraw = db.Column(db.Integer)
    
    

    def __repr__(self):
        return "<Post %r>" % self.id

    def serialize(self):
        return {
            'id': self.id,
            'current_balance': self.current_balance,
            'last_deposit': self.last_deposit,
            'last_withdraw': self.last_withdraw,
            
            
        }
    def serialize_just_name(self):
        return {
            'id': self.id,
            'current_balance': self.current_balance
            
        }