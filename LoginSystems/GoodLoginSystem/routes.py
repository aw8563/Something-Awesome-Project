from LoginSystems.GoodLoginSystem import app

@app.route('/')
def homePage():
    return "Good login system. TODO!"