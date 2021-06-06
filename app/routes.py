from app import *
from app.models import Users, Files


# pages
@app.route("/")
def main_page():
    return render_template("main.html")

# user pages
@app.route("/<string:username>")
def user_page(username):
    session.pop('_flashes', None)
    if 'user' in session:
        if username == session['user']:
            user = Users.query.filter_by(login=username).first()
            return render_template("user.html", login=username, email=user.email, name=user.name, surname=user.surname, age=user.age, gender=user.gender)
    return abort(403)

@app.route("/login", methods=['GET', 'POST'])
def login_page():
    if 'user' in session:
        return redirect(url_for('main_page'))
    elif request.method == 'POST':
        session.pop('_flashes', None)

        login = request.form.get("login")
        password = request.form.get("password")

        if login and password:
            user = Users.query.filter_by(login=login).first()
            if user:
                if check_password_hash(user.password, password):
                    session['user'] = login
                    flash("You has been succesfully logged in!", "success")
                    return redirect(url_for("main_page"))
                
                flash("The password is wrong!", "danger")
                return render_template("login.html")
            flash("There is no user with this login!", "warning")
            return render_template("login.html")
        flash("Fill the login and password rows!", "warning")
    return render_template("login.html")

@app.route("/register", methods=['POST', 'GET'])
def registration_page():
    if request.method == "POST":
        session.pop('_flashes', None)

        name = request.form['name']
        surname = request.form['surname']
        age = request.form['age']
        login = request.form['login']
        email = request.form['email']
        password = request.form['password']
        password_repeat = request.form['password-repeat']

        # remove errors
        try: gender = request.form['gender'] 
        except: gender = None
        if age == '': age = None
        
        success = (password == password_repeat and login != '' and password != '' and email != '' and not Users.query.filter_by(login=login) and not Users.query.filter_by(email=email))

        if success:
            password_hash = generate_password_hash(password)

            data = Users(name=name, surname=surname, email=email, login=login, password=password_hash, age=age, gender=gender)
            db.session.add(data)
            db.session.commit()

            session['user'] = login

            flash("You has been succesfully logged in!", "success")
            return redirect(url_for("main_page"))

        # error processing
        if password != password_repeat:
            flash("Passwords mismatch!", "danger")
        if login == '' or password == '' or email == '':
            flash("Fill all the rows with stars!", "danger")
        if Users.query.filter_by(login=login).first():
            flash("There is an other user with this login!", "warning")
        if Users.query.filter_by(email=email).first():
            flash("There is an other user with this email!", "warning")
    return render_template("registration.html")

@app.route("/logout")
def logout_page():
    session.pop('_flashes', None)
    session.pop('user', None)
    flash("You succesfully logged out!", "success")
    return redirect(url_for('login_page'))

@app.route("/delete-account")
def delete_account():
    if 'user' in session:
        session.pop('_flashes', None)
        session.pop('user', None)

        Users.query.filter_by(login=session['user']).delete()
        db.session.commit()

        flash("Your account has been succesfully deleted!", "success")
        return redirect(url_for('login_page'))
    return abort(403)

# file pages
@app.route("/<string:username>/files")
def files_page(username):
    if 'user' in session:
        if username == session['user']:
            files = db.session.query(Files).filter(Files.owner==username).all()
            return render_template("files.html", files=files, username=username)
    return abort(403)

# Remake this!!!
# @app.route("/files/download_all")
# def download_all():
#     return send_file("user_files/files.zip", as_attachment=True)

# @app.route("/<string:username>/files/upload", methods=['POST'])
# def upload_file(username):
#     if username == user.login.casefold() and user.logged_in:
#         file = request.files['inputFile']
#         user.file.push(file, user.login)

#         # updating local file data
#         user.file.data, user.file.ids = user.file.get_data(user.login)
#         return redirect(f"/{username}/files")
#     return abort(403)

@app.route("/<string:username>/files/download/<int:file_id>")
def download_file(username, file_id):
    if 'user' in session:
        if username == session['user']:
            file = Files.query.filter_by(id=file_id, owner=username).first()
            if file != None:
                return send_file(BytesIO(file.file), attachment_filename=file.filename, as_attachment=True)
        return abort(403)
    return abort(404)

@app.route("/<string:username>/files/delete/<int:file_id>")
def delete_file(username, file_id):
    if 'user' in session:
        if username == session['user']:
            Files.query.filter_by(id=file_id, owner=username).delete()
            db.session.commit()
            flash(f"File has been succesfully deleted!", "success")
            return redirect(f"/{username}/files")
        return abort(403)
    return abort(404)


# errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template("not_found.html"), 404

@app.errorhandler(403)
def page_not_found(e):
    return render_template("forbidden.html"), 403

# context processors
@app.context_processor
def get_login_info():
    login = ''
    logged_in = False
    if 'user' in session:
        login = session['user']
        logged_in = True
    return dict(login=login, logged_in=logged_in)
