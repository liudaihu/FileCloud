# Documentation



## Contents

[Installing packages](#Installing-packages)  
[Run the app](#Run-the-app)






### Installing packages

To use this app, you need to install Python 3.9 (it may works on other versions, but this is recommended).

You need to install pip 21 (recommended version).

You need to install this packages with pip:

```bash
bcrypt==3.2.0
cffi==1.14.5
click==8.0.1
cryptography==3.4.7
Flask==2.0.1
Flask-Bcrypt==0.7.1
Flask-Login==0.5.0
Flask-SQLAlchemy==2.5.1
greenlet==1.1.0
itsdangerous==2.0.1
Jinja2==3.0.1
MarkupSafe==2.0.1
psycopg2-binary==2.8.6
pycparser==2.20
six==1.16.0
SQLAlchemy==1.4.18
Werkzeug==2.0.1
```

For simply installing it, you may copy it to requirements.txt and run this command:

```bash
pip install -r requirements.txt
```





### Run the app

To run it on standard settings (http://127.0.0.1:5000/):

```bash
flask run
```

To run it on "8888" port:
```bash
flask run --port=8888
```

