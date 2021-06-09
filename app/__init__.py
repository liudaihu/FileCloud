from flask import *
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import os


# values for working with db
db_user = "artem"
db_name = "fcdb"
db_password = "password"
db_host = "localhost"
db_port = "5432"

# flask variables
app = Flask(__name__, static_folder=os.path.abspath('app/templates/static')) # for static files connection
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)

from app import models, routes, functions

app.secret_key = functions.generate_random_key(10, 20)
