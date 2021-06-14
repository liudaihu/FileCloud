from time import strftime

from flask import *
from flask_login import login_user, login_required, logout_user, current_user
from flask_bcrypt import check_password_hash
from loguru import logger

from app import app, db, login_manager, SALT
from app.models import *
from app.functions import *


# pages
@app.route("/")
def main_page():
    return render_template("main.html")


# user pages
@app.route("/<string:user_id>/")
@login_required
def user_page(user_id):
    if user_id == current_user.id:
        return render_template("user.html", username=current_user.username, email=current_user.email, name=current_user.name, surname=current_user.surname, age=current_user.age, gender=current_user.gender)
    return abort(403)


@app.route("/login/", methods=['GET', 'POST'])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for("user_page", user_id=current_user.id))
    elif request.method == 'POST':
        session.pop("_flashes", None)
        login = request.form.get("login").replace(' ', '')
        password = request.form.get("password").replace(' ', '')
        remember_me = request.form.get("remember_me") != None

        if login and password:
            user = get_user_login_data(login)
            if user:
                if check_password_hash(user.password, password+SALT):
                    login_user(user, remember=remember_me)
                    logger.info(f"User {user.id} logged in")
                    flash("You has been succesfully logged in!", "success")
                    return redirect(url_for("main_page"))
                flash("The password is wrong!", "danger")
                return render_template("login.html")
            flash("There is no user with this username or email!", "danger")
            return render_template("login.html")
        flash("Fill the username and password rows!", "warning")
    return render_template("login.html")


@app.route("/register/", methods=['POST', 'GET'])
def registration_page():
    if request.method == "POST":
        session.pop("_flashes", None)

        name = request.form['name'].replace(' ', '')
        surname = request.form['surname'].replace(' ', '')
        age = request.form['age']
        username = request.form['username'].replace(' ', '')
        email = request.form['email'].replace(' ', '')
        password = request.form['password'].replace(' ', '')
        password_repeat = request.form['password-repeat'].replace(' ', '')

        # remove exceptions
        try:
            gender = request.form['gender']
        except:
            gender = None

        if age == '':
            age = None

        if all_fields_match(password, password_repeat, email, username):
            user = create_user(password, name, surname,
                               email, username, age, gender)

            login_user(user)
            generate_user_key(user.id)

            logger.info(f"User {user.id} registered")
            flash("You has been succesfully registered!", "success")
            return redirect(url_for("main_page"))
        else:
            flashes = flash_fields_errors(
                password, password_repeat, email, username)
            for alert in flashes:
                flash(alert[0], alert[1])

    return render_template("registration.html")


@app.route("/logout/")
@login_required
def logout_page():
    account_name = current_user.id

    logout_user()

    logger.info(f"User {account_name} logged out")
    flash("You succesfully logged out!", "success")
    return redirect(url_for("login_page"))


@app.route("/delete-account/")
@login_required
def delete_account_page():
    account_name = current_user.id

    del_user(current_user)
    logout_user()

    logger.info(f"User {account_name} deleted")
    flash("Your account has been succesfully deleted!", "success")
    return redirect(url_for("login_page"))


# file pages
@app.route("/<string:user_id>/files/")
@login_required
def files_page(user_id):
    session.pop("_flashes", None)
    if user_id == current_user.id:
        files = db.session.query(Files).filter(Files.owner == user_id).all()
        return render_template("files.html", files=files)
    return abort(403)


@app.route("/<string:user_id>/files/download-all/")
@login_required
def download_all_files_page(user_id):
    key = get_user_key(user_id)
    archive = create_archive(user_id, key)
    logger.info("Archive created")
    return send_file(archive, attachment_filename="All files.zip", as_attachment=True)


@app.route("/<string:user_id>/files/upload/", methods=['POST'])
@login_required
def upload_file_page(user_id):
    session.pop("_flashes", None)
    if user_id == current_user.id:
        file = request.files['inputFile']
        upload_file(user_id, file)

        logger.info("File pushed to db")
        flash(
            f'File "{file.filename}" has been pushed to your disk!', "success")
        return redirect(url_for("files_page", user_id=current_user.id))
    return abort(403)


@app.route("/<string:user_id>/files/download/<string:file_id>/")
@login_required
def download_file_page(user_id, file_id):
    if user_id == current_user.id:
        file = Files.query.filter_by(id=file_id, owner=user_id).first()
        if file != None:
            dec_file = download_file(user_id, file.file)
            logger.info("File downloaded")
            return send_file(dec_file, attachment_filename=file.filename, as_attachment=True)
        return abort(404)
    return abort(403)


@app.route("/<string:user_id>/files/delete/<string:file_id>/")
@login_required
def delete_file_page(user_id, file_id):
    if user_id == current_user.id:
        del_file(user_id, file_id)
        logger.info("File deleted")
        flash(f"File has been succesfully deleted!", "success")
        return redirect(url_for("files_page", user_id=current_user.id))
    return abort(403)


# errors processing
@app.errorhandler(Exception)
def all_http_errors_handler(error):
    return render_template("error.html", err_code=error.code, err_desc=error.description), error.code


# logging
@app.after_request
def after_request(response):
    timestamp = strftime("[%d-%b-%Y %H:%M:%S]")
    url = request.remote_addr
    method = request.method
    path = request.full_path
    status = response.status

    if not "/static/" in path:
        global logger
        logger = logger.bind(url=url, timestamp=timestamp,
                             method=method, path=path, status=status)
        if status[0] == '5':
            logger.error('')
        elif status[0] == '4':
            logger.warning('')
        else:
            logger.debug('')

    return response


# load user for flask-login
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


# push data to html templates
@app.context_processor
def get_login_info():
    user_id, username, logged_in = get_template_data(current_user)
    return dict(user_id=user_id, username=username, logged_in=logged_in)
