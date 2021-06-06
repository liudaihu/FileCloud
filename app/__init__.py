from flask import *
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import os
from io import BytesIO
from werkzeug.security import generate_password_hash, check_password_hash
from random import randint
from datetime import date


# db login values
db_user = "artem"
db_name = "fcdb"

# flask variables
app = Flask(__name__, static_folder=os.path.abspath('app/templates/static')) # for static files connection
app.secret_key = 'some_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{db_user}:password@localhost:5432/{db_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
from app import models, routes
db.init_app(app)
