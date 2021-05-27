from init import *
from models import *


# errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template("not_found.html"), 404

# pages
@app.route("/")
def main_page():
    return render_template("main.html")

@app.route("/files")
def files_page():
    return render_template("files.html", files=file_data)

# Remake this!!!
# @app.route("/files/download_all")
# def download_all():
#     return send_file("user_files/files.zip", as_attachment=True)

@app.route("/files/upload", methods=['POST'])
def upload_file():
    file = request.files['inputFile']
    push_to_db(file)
    return redirect(url_for('files_page'))

@app.route("/files/download/<int:file_id>")
def download_file(file_id):
    if file_id in file_ids:
        downloaded_file = download_from_db(file_id)
        return send_file(BytesIO(downloaded_file.file), attachment_filename=downloaded_file.filename, as_attachment=True)
    return page_not_found(404)

@app.route("/files/delete/<int:file_id>")
def delete_file(file_id):
    if file_id in file_ids:
        delete_from_db(file_id)
        return redirect(url_for('files_page'))
    return page_not_found(404)
