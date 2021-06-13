import os

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


# values for working with db
db_user = "artem"
db_name = "fcdb"
db_password = "password"
db_host = "localhost"
db_port = "5432"

# for sqlite
db_path = "/mnt/c/Users/artte/Desktop/db.sqlite3"


# system environment variables
SALT = os.getenv('SALT')

# flask variables
app = Flask(__name__, static_folder=os.path.abspath(
    'app/templates/static'))  # for static files connection
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
app.config['SQLALCHEMY_BINDS'] = {
    "users_and_files":      f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}",
    "keys":                 f"sqlite:///{db_path}"
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager(app)


from app import models, routes, functions

app.secret_key = os.urandom(16)
