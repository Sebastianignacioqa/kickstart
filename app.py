from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Post
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:isac1234@localhost:5432/blog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
db.init_app(app)
Migrate(app, db)

@app.route ("/user", methods=["GET", "POST"])
def user():
    if request.method == "GET":
        user = User.query.get(1)
        return jsonify(user.serialize()), 200
    else:
        user = User()
        user.name = request.json.get("name")
        user.password = request.json.get("password")
        user.email = request.json.get("email")
        user.isActive = request.json.get("isActive")

        db.session.add(user)
        db.session.commit()

    return jsonify(user.serialize()), 200


if __name__== "__main__":
    app.run(host='localhost', port = 8080)
