from flask_login import UserMixin, login_user
import json

class User(UserMixin): # additional attributes when needed. For now just inherits from base class


    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def get_id(self):
        return self.id

    def __str__(self):
        return "USER: " + str(self.id)

class UserManager():
    def __init__(self):
        self.users = {} # empty map for now

        with open('LoginSystems/BadLoginSystem/userData.json') as jsonFile:
            data = json.load(jsonFile)
            for user in data['Users']:
                self.addUser(int(user['id']), user['username'], user['password'])


        for user in self.users.values():
            print(user)

    def addUser(self, id, username, password):
        self.users[username] = User(id, username, password)

    def getUser(self, id):
        print("getting id:", id)
        for user in self.users.values():
            if user.id == int(id):
                return user


    def loginUser(self, username, password):
        if username in self.users and password == self.users[username].password:
            login_user(self.users[username])
            return True

        return False