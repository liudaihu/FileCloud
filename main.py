from flask import *
from finder import files

app = Flask(__name__)

@app.route("/")
def main_page():
    return render_template("main.html", data=None)

@app.route("/files")
def files_page():
    return render_template("files.html", files=files)

