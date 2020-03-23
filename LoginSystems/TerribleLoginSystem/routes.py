from LoginSystems.TerribleLoginSystem import app

@app.route('/')
def homePage():
    return "Terrible login system. TODO!"