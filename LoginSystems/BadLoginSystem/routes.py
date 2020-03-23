from flask import render_template, request, redirect
from flask_login import login_required, login_user, logout_user, current_user

from LoginSystems.BadLoginSystem import app, userManager

@app.route('/')
def homePage():
    print(current_user)
    return render_template('home.html', user=current_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if (current_user.is_authenticated):
        return redirect('/')

    if request.method == "POST":
        username = request.form.get('Username')
        password = request.form.get('Password')

        if userManager.loginUser(username, password):

            login_user(userManager.users[username])
            return redirect('/')

    return render_template("loginPage.html")

@app.route('/logout')
def logoutUser():
    logout_user()
    return redirect('/')

@app.route('/secret')
@login_required
def secretPage():
    return "success!"