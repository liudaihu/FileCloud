from flask import *
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from io import BytesIO
from werkzeug.security import generate_password_hash, check_password_hash
from random import randint
from datetime import date


# db login values
class psql:
    user = "artem"
    db = "fcdb"

# just app global variables
class user:
    data = []
    logged_in = False
    login = ''

    LOGINS = []
    EMAILS = []

    class file:
        ids = []
        data = []


# flask variables
app = Flask(__name__)
app.secret_key = 'some_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{psql.user}:password@localhost:5432/{psql.db}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
db.init_app(app)
