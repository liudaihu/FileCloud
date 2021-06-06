from init import *
from models import Users, Files

# local functions
def get_user_auth():
    con = psycopg2.connect(dbname=psql.db, user=psql.user)
    cur = con.cursor()
    cur.execute("SELECT login, email FROM users;")
    data = cur.fetchall()
    cur.close()
    con.close()

    user_logins = []
    user_emails = []
    for elem in data:
        user_logins.append(elem[0])
        user_emails.append(elem[1])

    return user_logins, user_emails

# export functions for working with users
def create_user(name, surname, email, login, password, age, gender):
    age = None if age == '' else age
    data = Users(name=name, surname=surname, email=email, login=login, password=password, age=age, gender=gender)
    db.session.add(data)
    db.session.commit()

def get_user_data(login):
    con = psycopg2.connect(dbname=psql.db, user=psql.user)
    cur = con.cursor()
    cur.execute(f"SELECT email, name, surname, age, gender, password FROM users WHERE login = '{login}';")
    user_data = cur.fetchone()
    cur.close()
    con.close()

    return user_data

def delete_user(login):
    Users.query.filter_by(login=login).delete()
    db.session.commit()

    i = user.LOGINS.index(login)
    user.LOGINS.pop(i)
    user.EMAILS.pop(i)

# export functions for working with files
def get_file_data(login):
    con = psycopg2.connect(dbname=psql.db, user=psql.user)
    cur = con.cursor()
    cur.execute(f"SELECT id, filename, date FROM files WHERE owner = '{login}';")
    file_data = cur.fetchall()
    cur.close()
    con.close()

    file_ids = []
    for elem in file_data:
        file_ids.append(elem[0])

    return file_data, file_ids

def push_to_db(file, login):
    file_id = randint(1, 1000)
    while file_id in user.file.ids:
        file_id = randint(1, 1000)

    create_date = (date.today()).strftime("%d %B, %Y")

    data = Files(id=file_id, filename=file.filename, file=file.read(), date=create_date, owner=login)
    db.session.add(data)
    db.session.commit()

    # update local file data
    user.file.ids.append(file_id)
    user.file.data.append((file_id, file.filename, create_date, login)) # it's a tuple

def download_file(file_id):
    file = Files.query.filter_by(id=file_id).first()
    return file

def delete_file(file_id):
    Files.query.filter_by(id=file_id).delete()
    db.session.commit()

    # update local file data
    user.file.ids.remove(file_id)
    for i, j in enumerate(user.file.data):
        if j[0] == file_id:
            user.file.data.pop(i)

# exporting functions and variables
user.LOGINS, user.EMAILS = get_user_auth()
user.create = create_user
user.delete = delete_user
user.get_data = get_user_data
user.file.get_data = get_file_data
user.file.push = push_to_db
user.file.download = download_file
user.file.delete = delete_file
