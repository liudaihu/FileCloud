from random import randint, choice
from string import ascii_letters, digits
from flask_bcrypt import generate_password_hash
from werkzeug.utils import secure_filename
from io import BytesIO
import zipfile
from time import time, localtime
from cryptography.fernet import Fernet
from datetime import date

from app import db, SALT
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


def generate_user_key(user_id):
    key = Fernet.generate_key()
    key = key.decode('utf-8')
    user_key = Keys(owner=user_id, key=key)
    db.session.add(user_key)
    db.session.commit()


def get_user_key(user_id):
    key = Keys.query.filter_by(owner=user_id).first()
    key = bytes(key.key, 'utf-8')
    return key


def get_user_login_data(login):
    data = Users.query.filter_by(username=login).first()
    if not data:
        data = Users.query.filter_by(email=login).first()
        if not data:
            return None
    return data


def create_user(pswd, name, surname, email, username, age, gender):
    user_id = generate_user_id()
    pswd_hash = generate_password_hash(pswd+SALT)

    user = Users(id=user_id, name=name, surname=surname, email=email,
                 username=username, password=pswd_hash.decode('utf-8'), age=age, gender=gender)
    db.session.add(user)
    db.session.commit()

    return user


def del_user(user):
    Users.query.filter_by(id=user.id).delete()
    Files.query.filter_by(owner=user.id).delete()
    Keys.query.filter_by(owner=user.id).delete()
    db.session.commit()


def all_fields_match(pswd, pswd_repeat, email, username):
    username_row_mismatch = Users.query.filter_by(username=username).first()
    email_row_mismatch = Users.query.filter_by(email=email).first()
    success = (pswd == pswd_repeat and username != '' and pswd != '' and email !=
               '' and not username_row_mismatch and not email_row_mismatch)

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
        flashes.append(
            ("There is an other user with this username!", "warning"))
    if email_row_mismatch:
        flashes.append(("There is an other user with this email!", "warning"))
    return flashes


# files functions
def generate_file_id():
    file_id = generate_random_key()
    while Files.query.filter_by(id=file_id).first():
        file_id = generate_random_key()
    return file_id


def encrypt_file(read_file, key):
    fernet = Fernet(key)
    enc = fernet.encrypt(read_file)
    return enc


def decrypt_file(read_file, key):
    fernet = Fernet(key)
    dec = fernet.decrypt(read_file)
    return dec


def create_archive(user_id, key):
    files = db.session.query(Files).filter(Files.owner == user_id).all()

    archive = BytesIO()
    with zipfile.ZipFile(archive, mode='w') as zf:
        for file in files:
            data = zipfile.ZipInfo(file.filename)
            data.date_time = localtime(time())[:6]
            data.compress_type = zipfile.ZIP_DEFLATED
            fl = decrypt_file(file.file, key)
            zf.writestr(data, fl)
    archive.seek(0)
    return archive


def upload_file(owner, file):
    file_id = generate_file_id()

    creation_date = (date.today()).strftime("%d %B, %Y")

    key = get_user_key(owner)

    enc_file = encrypt_file(file.read(), key)

    filename = secure_filename(file.filename)

    data = Files(id=file_id, filename=filename,
                 file=enc_file, date=creation_date, owner=owner)
    db.session.add(data)
    db.session.commit()


def download_file(owner, read_file):
    key = get_user_key(owner)

    file = BytesIO(decrypt_file(read_file, key))
    return file


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
    "generate_user_key", "get_user_key", "get_user_login_data", "create_user", "del_user", "all_fields_match", "flash_fields_errors",
    # files_functions
    "create_archive", "upload_file", "download_file", "del_file",
    # app_functions
    "get_template_data"
]
