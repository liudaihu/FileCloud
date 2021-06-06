from flask import *
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import os
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

    # functions
    create = None
    get_data = None
    delete = None

    class file:
        ids = []
        data = []

        # functions
        get_data = None
        push = None
        download = None
        delete = None


# flask variables
app = Flask(__name__, static_folder=os.path.abspath('templates/static')) # for css connection
app.secret_key = 'some_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{psql.user}:password@localhost:5432/{psql.db}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
db.init_app(app)
