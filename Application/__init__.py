from flask import Flask
from flask_login import LoginManager, UserMixin


class User(UserMixin): # additional attributes when needed. For now just inherits from base class
    pass

app = Flask(__name__)
app.config.from_object("Application.config")





loginManager = LoginManager(app)

loginManager.login_view = 'login'



@loginManager.user_loader
def load_user(id):
    """
    Returns a User as specified by their User ID. This function is required by
    flask-login.
    :param id: The UID used to specify a particular User.
    :return: A User matching a specific UID. If no matches are found, returns None.
    """
    return User.get(id)

from Application import routes
