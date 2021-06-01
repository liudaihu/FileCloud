from init import *
from models import Users, Files

# getting user data when the server starts
def get_user_data():
    con = psycopg2.connect(dbname=db_name, user=db_user)
    cur = con.cursor()
    cur.execute("SELECT id, login FROM users;")
    user_data = cur.fetchall()
    cur.close()
    con.close()

    user_ids = []
    user_logins = []
    for elem in user_data:
        user_ids.append(elem[0])
        user_logins.append(elem[1])
    
    return user_ids, user_logins

# def get_file_data():
#     con = psycopg2.connect(dbname=db_name, user=db_user)
#     cur = con.cursor()
#     cur.execute("SELECT id, filename, date FROM files;")
#     file_data = cur.fetchall()
#     cur.close()
#     con.close()

#     file_ids = []
#     for elem in file_data:
#         file_ids.append(elem[0])

#     return file_data, file_ids

global user_ids, user_logins
user_ids, user_logins = get_user_data()
# file_data, file_ids = get_file_data()


# export functions for working with users
def register(name, surname, login, password, age, gender):
    user_id = randint(1, 1000)
    while user_id in user_ids:
        user_id = randint(1, 1000)
    if age == '':
        age = None
    user_data = Users(id=user_id, name=name, surname=surname, login=login, password=password, age=age, gender=gender)
    db.session.add(user_data)
    db.session.commit()


# export functions for working with files
# def push_to_db(file):
#     file_id = randint(1, 1000)
#     while file_id in file_ids:
#         file_id = randint(1, 1000)

#     create_date = (date.today()).strftime("%d %B, %Y")

#     export_data = Files(id=file_id, filename=file.filename, file=file.read(), date=create_date)
#     db.session.add(export_data)
#     db.session.commit()
    
#     # update local file data
#     file_ids.append(file_id)
#     file_data.append((file_id, file.filename, create_date))

# def download_from_db(file_id):
#     file = Files.query.filter_by(id=file_id).first()
#     return file

# def delete_from_db(file_id):
#     global file_data
#     Files.query.filter_by(id=file_id).delete()
#     db.session.commit()

#     # update local file data
#     file_ids.remove(file_id)
#     for i, j in enumerate(file_data):
#         if j[0] == file_id:
#             file_data.pop(i)
