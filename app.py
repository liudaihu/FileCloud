from init import *
from db import push_to_db, file_indexes, file_names, Files

cprint(file_indexes, color='red')
cprint(file_names, color='cyan')

@app.route("/")
def main_page():
    return render_template("main.html")

@app.route("/files")
def files_page():
    return render_template("files.html", file_indexes=file_indexes, files=file_names)

@app.route("/files/download_all")
def download_all():
    return send_file("user_files/files.zip", as_attachment=True)

@app.route("/files/<int:file_id>")
def download_file(file_id):
    if file_id in file_indexes:
        rf = Files.query.filter_by(id=file_id).first()
        return send_file(BytesIO(rf.file), attachment_filename=rf.filename, as_attachment=True)
    return 'Error 404: Page not found'

@app.route("/files/upload", methods=['POST'])
def upload_file():
    f = request.files['inputFile']
    push_to_db(f)

    return redirect(url_for('files_page'))
