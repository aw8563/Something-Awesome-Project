from flask_login import UserMixin, login_user
import json

DATA_PATH = "LoginSystems/BadLoginSystem/userData.json"

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
        self.id = 0

        self.loadUsers()


    def loadUsers(self):
        with open(DATA_PATH) as jsonFile:
            data = json.load(jsonFile)
            for user in data['Users']:
                username = user['username']
                password = user['password']
                id = user['id']

                self.users[username] = User(id, username, password)

                if (self.id <= id):
                    self.id = id + 1

    def newUser(self, username, password):
        if (username == "" or username in self.users):
            return

        if not self.checkStrength(password):
            return

        self.users[username] = User(self.id, username, password)

        with open(DATA_PATH) as jsonFile:
            data = json.load(jsonFile)
            newUser = {"id":self.id, "username":username, "password":password}
            data['Users'].append(newUser)

        with open(DATA_PATH, "w") as jsonFile:
            json.dump(data, jsonFile, indent=4)

        self.id += 1
        return self.users[username]

    def getUser(self, id):
        for user in self.users.values():
            if user.id == int(id):
                return user


    def loginUser(self, username, password):
        if username in self.users and password == self.users[username].password:
            login_user(self.users[username])
            return True

        return False

    # make sure password is ok
    # for the bad login system this will only that it is not empty!
    def checkStrength(self, password):
        return len(password) > 0