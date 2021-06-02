from init import *
from db_manager import register, get_user_data, user_logins # TODO: do something with this shit!!!


# pages
@app.route("/")
def main_page():
    return render_template("main.html", logged_in=logged_in, login=login)

# user pages
# @app.route("/" + login.casefold())
@app.route("/<string:username>")
def user_page(username):
    if username == login.casefold() and logged_in:
        return render_template("user.html", login=login, email=user_data[0], name=user_data[1], surname=user_data[2], age=user_data[3], gender=user_data[4])
    return abort(404)

    # if logged_in:
    #     print(f"Login - {login}")
    #     return render_template("user.html", login=login, email=user_data[0], name=user_data[1], surname=user_data[2], age=user_data[3], gender=user_data[4])
    # return page_not_found(404)

@app.route("/login", methods=['GET', 'POST'])
def login_page():
    session.pop('_flashes', None)

    global logged_in, login, user_data
    if logged_in:
        return redirect(url_for('main_page'))
    elif request.method == 'POST':
        user_data = get_user_data(request.form['login'])
        if user_data != None:
            if check_password_hash(user_data[5], request.form['password']):
                # updating local user data
                login = request.form['login']
                session['user'] = login
                logged_in = True
                user_data = get_user_data(login)
                user_logins.append(login)

                return redirect(f'/{login.casefold()}')
            flash("The password is wrong!", "error")
        flash("This login is wrong", "error")
    return render_template("login.html")

@app.route("/register", methods=['POST', 'GET'])
def registration_page():
    if request.method == "POST":
        session.pop('_flashes', None)

        global logged_in, login, user_data, user_logins
        # if all is ok
        if request.form['password'] == request.form['password-repeat'] and request.form['login'] != '' \
            and request.form['password'] != '' and request.form['login'] not in user_logins and request.form['email'] != '':
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
            login = request.form['login']
            session['user'] = login
            logged_in = True
            user_data = get_user_data(login)
            user_logins.append(login)
            return redirect(f'/{login.casefold()}')

        # error processing
        if request.form['password'] != request.form['password-repeat']:
            flash("Password mismatch!", "error")

        if request.form['login'] == '' or request.form['password'] == '' or request.form['email'] == '': # TODO: add email primary key
            flash("Please fill the rows with stars!", "error")

        if request.form['login'] in user_logins:
            flash("We already have user with this login!", "error")
        
    return render_template("registration.html")

@app.route("/logout")
def logout_page():
    global logged_in, login, user_data
    session.pop('_flashes', None)
    # updating local user data
    session.pop('user', None)
    logged_in = False
    login = None
    user_data = None
    flash("You succesfully logged out!", "info")
    return redirect(url_for('login_page'))




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
