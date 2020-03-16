from flask import render_template
from flask_login import current_user, login_required, login_user, logout_user, current_user

from Application import app, loginManager


@app.route('/')
def homePage():
    logout_user()

    return render_template('home.html')

@app.route('/login')
def login():
    return "LOGIN PAGE"


@login_required
@app.route('/secret')
def secretPage():
    return "you are logged in!"