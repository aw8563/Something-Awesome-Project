from flask import render_template, request, redirect
from flask_login import login_required, login_user, logout_user, current_user

from LoginSystems.AverageLoginSystem import app, databaseManager

@app.route('/')
def homePage():
    return render_template('home.html')

@app.route('/createAccount', methods=["GET", "POST"])
def createAccount():
    if (current_user.is_authenticated):
        return redirect('/')

    if request.method == 'POST':
        # creating new acct
        username = request.form.get('Username')
        password = request.form.get('Password')

        user = databaseManager.addUser(username, password)
        if (user):
            login_user(user)
            return redirect('/')
        else:
            return render_template("createAccount.html", error=True)

    return render_template('createAccount.html', error=False)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # TODO: this 'next' is EXTREMELY unsafe. An attacker could use this to redirect victims a new phising website upon login
    next = request.args.get('next')
    if (current_user.is_authenticated):
        return redirect(next or '/')

    if request.method == "POST":
        username = request.form.get('Username')
        password = request.form.get('Password')

        if databaseManager.loginUser(username, password):
            return redirect(next or '/')

    return render_template("loginPage.html")

@app.route('/logout')
def logoutUser():
    logout_user()
    return redirect('/')

@app.route('/secret')
@login_required
def secretPage():
    return "success!"


@app.route('/search', methods=['GET', 'POST'])
def searchPage():
    search = False
    results = []
    if request.method == 'POST':
        query = request.form.get('query')
        results = databaseManager.query(query)
        search=True

    return render_template('searchPage.html', search=search, results=results)