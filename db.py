from init import *

# Models
class Files(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    filename = db.Column(db.Text, nullable=False)
    file = db.Column(db.BINARY)

# local values
def get_file_data():
    all_files = Files.query.all()
    file_indexes = []
    file_names = []
    for file in all_files:
        file_indexes.append(file.id)
        file_names.append(file.filename)
    return file_indexes, file_names

# export values
file_indexes, file_names = get_file_data()

def push_to_db(fl):
    f_id = (file_indexes[-1])+1
    data = Files(id=f_id, filename=fl.filename, file=fl.read())
    db.session.add(data)
    db.session.commit()
    file_indexes.append(f_id)
    file_names.append(fl.filename)
