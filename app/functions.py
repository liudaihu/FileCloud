from random import randint, choice
from string import ascii_letters, digits
from werkzeug.security import generate_password_hash
from datetime import date

from app import db
from app.models import *


symbols = ascii_letters + digits


# local functions
def generate_random_key(min_len=2, max_len=10):
    key = ""
    for i in range(randint(min_len, max_len)):
        key += choice(symbols)
    return key


# user functions
def generate_user_id():
    user_id = generate_random_key()
    while Users.query.filter_by(id=user_id).first():
        user_id = generate_random_key()
    return user_id

def get_user_login_data(login):
    data = Users.query.filter_by(username=login).first()
    if not data:
        data = Users.query.filter_by(email=login).first()
        if not data:
            return None
    return data

def create_user(pswd, name, surname, email, username, age, gender):
    user_id = generate_user_id()
    pswd_hash = generate_password_hash(pswd)

    user = Users(id=user_id, name=name, surname=surname, email=email, username=username, password=pswd_hash, age=age, gender=gender)
    db.session.add(user)
    db.session.commit()

    return user

def del_user(user):
    Users.query.filter_by(id=user.id).delete()
    Files.query.filter_by(owner=user.id).delete()
    db.session.commit()

def all_fields_match(pswd, pswd_repeat, email, username):
    username_row_mismatch = Users.query.filter_by(username=username).first()
    email_row_mismatch = Users.query.filter_by(email=email).first()
    success = (pswd == pswd_repeat and username != '' and pswd != '' and email != '' and not username_row_mismatch and not email_row_mismatch)

    return success

def flash_fields_errors(pswd, pswd_repeat, email, username):
    flashes = []

    username_row_mismatch = Users.query.filter_by(username=username).first()
    email_row_mismatch = Users.query.filter_by(email=email).first()

    if pswd != pswd_repeat:
        flashes.append(("Passwords mismatch!", "danger"))
    if username == '' or pswd == '' or email == '':
        flashes.append(("Fill all the rows with stars!", "danger"))
    if username_row_mismatch:
        flashes.append(("There is an other user with this username!", "warning"))
    if email_row_mismatch:
        flashes.append(("There is an other user with this email!", "warning"))
    return flashes


# files functions
def generate_file_id():
    file_id = generate_random_key()
    while Files.query.filter_by(id=file_id).first():
        file_id = generate_random_key()
    return file_id

def upload_file(owner, file):
    file_id = generate_file_id()

    creation_date = (date.today()).strftime("%d %B, %Y")

    data = Files(id=file_id, filename=file.filename, file=file.read(), date=creation_date, owner=owner)
    db.session.add(data)
    db.session.commit()

def del_file(owner, file_id):
    Files.query.filter_by(id=file_id, owner=owner).delete()
    db.session.commit()


# app functions
def get_template_data(user):
    try:
        user_id = user.id
        username = user.username
        logged_in = user.is_authenticated
    except: 
        user_id = ''
        username = ''
        logged_in = False
    return user_id, username, logged_in


__all__ = [
    # user_functions
    "get_user_login_data", "create_user", "del_user", "all_fields_match", "flash_fields_errors",
    # files_functions
    "upload_file", "del_file",
    # app_functions
    "get_template_data"
]
