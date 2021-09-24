from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id= db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    isActive = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return "<User %r>" % self.id

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'password': self.password,
            'email': self.email,
            'isActive': self.isActive
        }
    def serialize_just_username(self):
        return {
            'id': self.id,
            'name': self.name
        }

class Post(db.Model):
    __tablename__ = 'post'
    id= db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    user = db.relationship("User", backref=db.backref("user", lazy = True))

    def __repr__(self):
        return "<Post %r>" % self.id

    def serialize(self):
        return {
            'user_id': self.user_id,
            'id': self.id,
            'name': self.name,
            'description': self.description
        }
    def serialize_just_userid(self):
        return {
            'user_id': self.user_id 
        }