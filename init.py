from flask import *
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from termcolor import cprint # delete it from pip

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://artem:password@localhost:5432/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
db.init_app(app)
