from flask import *
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import os

from app.functions import generate_random_key


# db login values
db_user = "artem"
db_name = "fcdb"
db_password = "password"
db_host = "localhost"
db_port = "5432"

# flask variables
app = Flask(__name__, static_folder=os.path.abspath('app/templates/static')) # for static files connection
app.secret_key = generate_random_key(10, 20)
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.init_app(app)
login_manager = LoginManager(app)

from app import models, routes
