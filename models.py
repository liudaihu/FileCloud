from init import *

# Models
class Files(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    filename = db.Column(db.String(40), nullable=False)
    file = db.Column(db.BINARY, nullable=False)
    date = db.Column(db.String(20), nullable=False)

def get_file_data():
    con = psycopg2.connect(dbname="fcdb", user="artem")
    cur = con.cursor()
    cur.execute("SELECT id, filename, date FROM files;")
    file_data = cur.fetchall()
    cur.close()
    con.close()

    file_ids = []
    for elem in file_data:
        file_ids.append(elem[0])

    return file_data, file_ids

file_data, file_ids = get_file_data()

def push_to_db(file):
    file_id = randint(1, 1000)
    while file_id in file_ids:
        file_id = randint(1, 1000)

    create_date = (date.today()).strftime("%d %B, %Y")

    export_data = Files(id=file_id, filename=file.filename, file=file.read(), date=create_date)
    db.session.add(export_data)
    db.session.commit()
    
    # update local file data
    file_ids.append(file_id)
    file_data.append((file_id, file.filename, create_date))

def download_from_db(file_id):
    file = Files.query.filter_by(id=file_id).first()
    return file

def delete_from_db(file_id):
    global file_data
    Files.query.filter_by(id=file_id).delete()
    db.session.commit()

    # update local file data
    file_ids.remove(file_id)
    for i, j in enumerate(file_data):
        if j[0] == file_id:
            file_data.pop(i)
