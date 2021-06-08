from flask_login import UserMixin

from app import app, db, login_manager


# Models
class Users(db.Model, UserMixin):
    id = db.Column(db.String(10), primary_key=True, nullable=False)
    name = db.Column(db.String(64))
    surname = db.Column(db.String(64))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(1))
    email = db.Column(db.String(128), unique=True, nullable=False)
    login = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(512), nullable=False)

class Files(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    filename = db.Column(db.String(40), nullable=False)
    file = db.Column(db.BINARY, nullable=False)
    date = db.Column(db.String(20), nullable=False)
    owner = db.Column(db.String(40), nullable=False)
