from random import randint, choice
from string import ascii_letters, digits
from datetime import date

# from app import db
# from app.models import Files

symbols = ascii_letters + digits

def generate_random_key(min_len=2, max_len=10):
    key = ""
    for i in range(randint(min_len, max_len)):
        key += choice(symbols)
    return key

# def upload_file(owner, file, db, Files):
#     file_id = randint(1, 1000)
#     while Files.query.filter_by(id=file_id).first():
#         file_id = randint(1, 1000)

#     creation_date = (date.today()).strftime("%d %B, %Y")

#     data = Files(id=file_id, filename=file.filename, file=file.read(), date=creation_date, owner=owner)
#     db.session.add(data)
#     db.session.commit()
