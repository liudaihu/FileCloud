from flask import *
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from io import BytesIO
from random import randint
from datetime import date


# flask variables
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://artem:password@localhost:5432/fcdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
db.init_app(app)
