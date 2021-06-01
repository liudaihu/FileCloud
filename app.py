from init import *
from db_manager import *


# pages
@app.route("/")
def main_page():
    global logged_in, name
    if 'user' in session:
        logged_in = True
        name = session['user']
    else:
        logged_in = False
        name = None
    return render_template("main.html", logged_in=logged_in, name=name)

# user pages
@app.route("/user")
def user_page():
    global logged_in, name
    if 'user' in session:
        logged_in = True
        name = session['user']
        return render_template("user.html", logged_in=logged_in, name=name)
    else:
        logged_in = False
        name = None
    return page_not_found(404)

@app.route("/user/login")
def login():
    return render_template("login.html")

@app.route("/user/register", methods=['POST', 'GET'])
def registration():
    if request.method == "POST":
        session.pop('_flashes', None)
        if len(request.form['login']) > 5 and len(request.form['password']) > 5 and request.form['password'] == request.form['password-repeat']:
            password_hash = generate_password_hash(request.form['password'])
            register(name=request.form['name'], surname=request.form['surname'], login=request.form['login'],\
                password=password_hash, age=request.form['age'], gender=request.form['gender'])
            session['user'] = request.form['login']
            return redirect(url_for('user_page'))
        else:
            flash("There is an error in form inputs!", "error")
    return render_template("registration.html")

@app.route("/user/logout")
def logout():
    session.pop("user", None)
    flash("You succesfully logged out!", "info")
    return redirect(url_for('login'))




# file pages
# @app.route("/files")
# def files_page():
#     return render_template("files.html", files=file_data)

# Remake this!!!
# @app.route("/files/download_all")
# def download_all():
#     return send_file("user_files/files.zip", as_attachment=True)

# @app.route("/files/upload", methods=['POST'])
# def upload_file():
#     file = request.files['inputFile']
#     push_to_db(file)
#     return redirect(url_for('files_page'))

# @app.route("/files/download/<int:file_id>")
# def download_file(file_id):
#     if file_id in file_ids:
#         downloaded_file = download_from_db(file_id)
#         return send_file(BytesIO(downloaded_file.file), attachment_filename=downloaded_file.filename, as_attachment=True)
#     return abort(404)

# @app.route("/files/delete/<int:file_id>")
# def delete_file(file_id):
#     if file_id in file_ids:
#         delete_from_db(file_id)
#         return redirect(url_for('files_page'))
#     return abort(404)


# errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template("not_found.html"), 404
