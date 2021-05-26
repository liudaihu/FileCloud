from init import *
from file_manager import files, file_indexes
from db import push_to_db

@app.route("/")
def main_page():
    return render_template("main.html")

@app.route("/files")
def files_page():
    return render_template("files.html", file_indexes=file_indexes, files=files)

@app.route("/files/download_all")
def download_all():
    return send_file("user_files/files.zip", as_attachment=True, cache_timeout=-1)

@app.route("/files/<int:file_id>")
def download_file(file_id):
    if file_id in file_indexes:
        return send_file(f"user_files/{files[file_id]}", as_attachment=True, cache_timeout=-1)
    return 'Error 404: Page not found'

@app.route("/files/upload", methods=['POST'])
def upload_file():
    f = request.files['inputFile']
    push_to_db(f)

    return f'File {f.filename} has been pushed to db!'

# stop caching files
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response
