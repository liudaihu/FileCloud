from flask import *
from file_manager import files

app = Flask(__name__)

@app.route("/")
def main_page():
    return render_template("main.html")

@app.route("/files")
def files_page():
    return render_template("files.html", files=files)

@app.route("/files/download_all")
def download_all():
    return send_file("user_files/files.zip", as_attachment=True)
