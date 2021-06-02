from flask import *
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from io import BytesIO
from werkzeug.security import generate_password_hash, check_password_hash
from random import randint
from datetime import date


# db login values
db_user = "artem"
db_name = "fcdb"

# just app global variables
user_logins = None
user_data = None
logged_in = False
login = None

# flask variables
app = Flask(__name__)
app.secret_key = 'some_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{db_user}:password@localhost:5432/{db_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
db.init_app(app)
