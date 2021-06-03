from init import *
from db_manager import *


# pages
@app.route("/")
def main_page():
    return render_template("main.html", logged_in=user.logged_in, login=user.login)

# user pages
@app.route("/<string:username>")
def user_page(username):
    if username == user.login.casefold() and user.logged_in:
        return render_template("user.html", login=user.login, email=user.data[0], name=user.data[1], surname=user.data[2], age=user.data[3], gender=user.data[4])
    return abort(404)

@app.route("/login", methods=['GET', 'POST'])
def login_page():
    if user.logged_in:
        return redirect(url_for('main_page'))
    elif request.method == 'POST':
        session.pop('_flashes', None)
        user.data = get_user_data(request.form['login'])
        if user.data != None:
            if check_password_hash(user.data[5], request.form['password']):
                # updating local user data
                user.login = request.form['login']
                session['user'] = user.login
                user.logged_in = True
                user.data = get_user_data(user.login)

                # updating local file data
                user.file.data, user.file.ids = get_file_data(user.login)

                return redirect(f'/{user.login.casefold()}')
            flash("The password is wrong!", "danger")
        flash("This login is wrong", "danger")
    return render_template("login.html")

@app.route("/register", methods=['POST', 'GET'])
def registration_page():
    if request.method == "POST":
        session.pop('_flashes', None)

        # if all is ok
        success = request.form['password'] == request.form['password-repeat'] and request.form['login'] != '' and request.form['password'] != '' and request.form['email'] != '' and request.form['login'].casefold() not in (login.casefold() for login in user.LOGINS) and request.form['email'].casefold() not in (email.casefold() for email in user.EMAILS)

        if success:
            password_hash = generate_password_hash(request.form['password'])
            register(
                name=request.form['name'],
                surname=request.form['surname'],
                email=request.form['email'],
                login=request.form['login'],
                password=password_hash,
                age=request.form['age'],
                gender=request.form['gender']
            )

            # updating local user data
            user.login = request.form['login']
            session['user'] = request.form['login']
            user.logged_in = True
            user.data = get_user_data(request.form['login'])
            user.LOGINS.append(request.form['login'])
            user.EMAILS.append(request.form['email'])

            return redirect(f'/{user.login.casefold()}')

        # error processing
        if request.form['password'] != request.form['password-repeat']:
            flash("Password mismatch!", "danger")

        if request.form['login'] == '' or request.form['password'] == '' or request.form['email'] == '':
            flash("Please fill the rows with stars!", "danger")

        if request.form['login'] in user.LOGINS:
            flash("We already have user with this login!", "warning")

        if request.form['email'] in user.EMAILS:
            flash("We already have user with this email!", "warning")
        
    return render_template("registration.html")

@app.route("/logout")
def logout_page():
    session.pop('_flashes', None)

    # updating local user data
    session.pop('user', None)
    user.logged_in = False
    user.login = ''
    user.data = []
    user.file.data = []

    flash("You succesfully logged out!", "success")
    return redirect(url_for('login_page'))


# file pages
@app.route("/<string:username>/files")
def files_page(username):
    if username == user.login.casefold() and user.logged_in:
        return render_template("files.html", files=user.file.data, username=username)
    return abort(404)

# Remake this!!!
# @app.route("/files/download_all")
# def download_all():
#     return send_file("user_files/files.zip", as_attachment=True)

@app.route("/<string:username>/files/upload", methods=['POST'])
def upload_file(username):
    if username == user.login.casefold() and user.logged_in:
        file = request.files['inputFile']
        push_to_db(file, user.login)

        # updating local file data
        user.file.data, user.file.ids = get_file_data(user.login)
        return redirect(f"/{username}/files")
    return abort(404)

@app.route("/<string:username>/files/download/<int:file_id>")
def download_file(username, file_id):
    if username == user.login.casefold() and user.logged_in and file_id in user.file.ids:
        file = download_from_db(file_id)
        return send_file(BytesIO(file.file), attachment_filename=file.filename, as_attachment=True)
    return abort(404)

@app.route("/<string:username>/files/delete/<int:file_id>")
def delete_file(username, file_id):
    if username == user.login.casefold() and user.logged_in and file_id in user.file.ids:
        delete_from_db(file_id)
        return redirect(f"/{username}/files")
    return abort(404)


# errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template("not_found.html"), 404
