from init import *

# Models
class Files(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    filename = db.Column(db.Text, nullable=False)
    file = db.Column(db.BINARY)

def get_file_data():
    con = psycopg2.connect(dbname="test", user="artem")
    cur = con.cursor()
    cur.execute("SELECT id, filename FROM files;")
    all_data = cur.fetchall()
    cur.close()
    con.close()

    f_data = {}
    for i in all_data:
        # i[o] - id, i[1] - filename
        f_data[str(i[0])] = i[1]
    return f_data

file_data = get_file_data()

def push_to_db(fl):
    f_id = 1
    while str(f_id) in file_data:
        f_id = randint(1, 1000)
    data = Files(id=f_id, filename=fl.filename, file=fl.read())
    db.session.add(data)
    db.session.commit()
    file_data[str(f_id)] = fl.filename

def download_from_db(f_id):
    fl = Files.query.filter_by(id=f_id).first()
    return fl

def delete_from_db(f_id):
    global file_data
    Files.query.filter_by(id=f_id).delete()
    db.session.commit()
    file_data.pop(str(f_id)) # update local file data
