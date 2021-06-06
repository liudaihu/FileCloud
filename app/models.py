from app import db

# Models
class Users(db.Model):
    name = db.Column(db.String(20))
    surname = db.Column(db.String(20))
    email = db.Column(db.String(40))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(1))
    login = db.Column(db.String(40), primary_key=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)

class Files(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    filename = db.Column(db.String(40), nullable=False)
    file = db.Column(db.BINARY, nullable=False)
    date = db.Column(db.String(20), nullable=False)
    owner = db.Column(db.String(40), nullable=False)
