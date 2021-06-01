from init import db

# Models
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(15))
    surname = db.Column(db.String(15))
    login = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(1))

class Files(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    filename = db.Column(db.String(40), nullable=False)
    file = db.Column(db.BINARY, nullable=False)
    date = db.Column(db.String(20), nullable=False)
