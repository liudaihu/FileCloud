from flask import *
from flask_login import login_user, login_required, logout_user, current_user
from io import BytesIO
from werkzeug.security import generate_password_hash, check_password_hash

from random import randint, choice
from datetime import date

from app import app, db, login_manager
from app.models import Users, Files
from app.functions import generate_random_key#, upload_file


# pages
@app.route("/")
def main_page():
    return render_template("main.html")

# user pages
@app.route("/<string:user_id>")
@login_required
def user_page(user_id):
    session.pop('_flashes', None)
    if user_id == current_user.id:
        return render_template("user.html", login=current_user.login, email=current_user.email, name=current_user.name, surname=current_user.surname, age=current_user.age, gender=current_user.gender)
    return abort(403)

@app.route("/login", methods=['GET', 'POST'])
def login_page():
    if current_user.is_authenticated:
        return redirect(f"/{current_user.id}")
    if request.method == 'POST':
        session.pop('_flashes', None)

        login = request.form.get("login")
        password = request.form.get("password")

        if login and password:
            user = Users.query.filter_by(login=login).first()
            if user and check_password_hash(user.password, password):
                login_user(user)
                flash("You has been succesfully logged in!", "success")
                return redirect(url_for("main_page"))
            elif not check_password_hash(user.password, password):
                flash("The password is wrong!", "danger")
                return render_template("login.html")
            else:
                flash("There is no user with this login!", "warning")
                return render_template("login.html")
        flash("Fill the login and password rows!", "warning")
    return render_template("login.html")

@app.route("/register", methods=['POST', 'GET'])
def registration_page():
    session.pop('_flashes', None)
    if request.method == "POST":
        name = request.form['name']
        surname = request.form['surname']
        age = request.form['age']
        login = request.form['login']
        email = request.form['email']
        password = request.form['password']
        password_repeat = request.form['password-repeat']

        # remove exceptions
        try: gender = request.form['gender'] 
        except: gender = None

        if age == '': age = None

        user_id = generate_random_key()
        while Users.query.filter_by(id=user_id).first():
            user_id = generate_random_key()

        user_login_mismatch = Users.query.filter_by(login=login).first()
        user_email_mismatch = Users.query.filter_by(email=email).first()

        success = (password == password_repeat and login != '' and password != '' and email != '' and not user_login_mismatch and not user_email_mismatch)

        if success:
            password_hash = generate_password_hash(password)

            data = Users(id=user_id, name=name, surname=surname, email=email, login=login, password=password_hash, age=age, gender=gender)
            db.session.add(data)
            db.session.commit()

            login_user(Users.query.filter_by(id=user_id).first())

            flash("You has been succesfully registered!", "success")
            return redirect(url_for("main_page"))

        # error processing
        if password != password_repeat:
            flash("Passwords mismatch!", "danger")
        if login == '' or password == '' or email == '':
            flash("Fill all the rows with stars!", "danger")
        if user_login_mismatch:
            flash("There is an other user with this login!", "warning")
        if user_email_mismatch:
            flash("There is an other user with this email!", "warning")
    return render_template("registration.html")

@app.route("/logout")
@login_required
def logout_page():
    session.pop('_flashes', None)
    logout_user()
    flash("You succesfully logged out!", "success")
    return redirect(url_for('login_page'))

@app.route("/delete-account")
@login_required
def delete_account_page():
    session.pop('_flashes', None)
    Users.query.filter_by(id=current_user.id).delete()
    Files.query.filter_by(owner=current_user.id).delete()
    logout_user()
    db.session.commit()

    flash("Your account has been succesfully deleted!", "success")
    return redirect(url_for('login_page'))


# file pages
@app.route("/<string:user_id>/files")
@login_required
def files_page(user_id):
    if user_id == current_user.id:
        files = db.session.query(Files).filter(Files.owner==user_id).all()
        return render_template("files.html", files=files)
    return abort(403)

# Remake this!!!
# @app.route("/files/download_all")
# def download_all_files_page():
#     return send_file("user_files/files.zip", as_attachment=True)

@app.route("/<string:user_id>/files/upload", methods=['POST'])
@login_required
def upload_file_page(user_id):
    if user_id == current_user.id:
        file = request.files['inputFile']
        file_id = randint(1, 1000)
        while Files.query.filter_by(id=file_id).first():
            file_id = randint(1, 1000)

        creation_date = (date.today()).strftime("%d %B, %Y")

        data = Files(id=file_id, filename=file.filename, file=file.read(), date=creation_date, owner=user_id)
        db.session.add(data)
        db.session.commit()

        flash(f'File "{file.filename}" has been pushed to your disk!', "success")
        return redirect(f"/{user_id}/files")
    return abort(403)

@app.route("/<string:user_id>/files/download/<int:file_id>")
@login_required
def download_file_page(user_id, file_id):
    if user_id == current_user.id:
        file = Files.query.filter_by(id=file_id, owner=user_id).first()
        if file != None:
            return send_file(BytesIO(file.file), attachment_filename=file.filename, as_attachment=True)
        return abort(404)
    return abort(403)

@app.route("/<string:user_id>/files/delete/<int:file_id>")
@login_required
def delete_file_page(user_id, file_id):
    if user_id == current_user.id:
        Files.query.filter_by(id=file_id, owner=user_id).delete()
        db.session.commit()
        flash(f"File has been succesfully deleted!", "success")
        return redirect(f"/{user_id}/files")
    return abort(403)


# errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template("not_found.html"), 404

@app.errorhandler(403)
def page_not_found(e):
    return render_template("forbidden.html"), 403


# load user for flask-login
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


# push data to html templates
@app.context_processor
def get_login_info():
    try: 
        user_id = current_user.id
        login = current_user.login
    except: user_id = login = ""
    return dict(user_id=user_id, login=login, logged_in=current_user.is_authenticated)
