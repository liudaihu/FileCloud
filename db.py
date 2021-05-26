from init import *

id_num = 1

class Files(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    filename = db.Column(db.Text, nullable=False)
    file = db.Column(db.BINARY)

def push_to_db(fl):
    global id_num
    data = Files(id=id_num, filename=fl.filename, file=fl.read())
    db.session.add(data)
    db.session.commit()
    id_num += 1
