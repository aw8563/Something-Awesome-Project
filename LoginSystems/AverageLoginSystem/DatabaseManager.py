from flask_login import UserMixin, login_user
import sqlite3

DATABASE_PATH = "LoginSystems/AverageLoginSystem/database.db"
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def get_id(self):
        return self.id

    def __str__(self):
        return "ID: %d | Username: %s | Password %s" %(self.id, self.username, self.password)


class DatabaseManager():
    def __init__(self):
        self.database = sqlite3.connect(DATABASE_PATH, check_same_thread=False)

    def getUser(self, id):
        result = self.database.execute("select * from Users where id = %d" % id).fetchone()

        if (result):
            return User(result[0], result[1], result[2])


    def addUser(self, username, password):
        if not self.checkPassword(password):
            return

        if self.database.execute("select * from Users where username ='%s' limit 1" % username).fetchone():
            return

        self.database.execute("insert into Users (username, password) values('%s', '%s')" % (username, password))
        self.database.commit()

        result = self.database.execute("select * from Users where username = '%s'" %username).fetchone()

        return User(result[0], result[1], result[2])

    def checkPassword(self, password):
        return len(password) > 6

    def loginUser(self, username, password):
        result = self.database.execute("select * from Users where username = '%s' and password = '%s' limit 1" %
                                       (username, password)).fetchone()

        if result:
            login_user(User(result[0], result[1], result[2]))
            return True

        return False

    def query(self, value):
        return self.database.execute("select * from Items where name like '%s' or id = %s"
                                     % ('%'+value+'%', value if value.isdigit() else -1)).fetchall() or []


database = sqlite3.connect("database.db")
# database.execute("DROP TABLE USERS")
# database.execute("CREATE TABLE USERS(id INTEGER PRIMARY KEY AUTOINCREMENT , username varchar(255), password varchar(255))")

# for result in database.execute("SELECT * FROM USERS").fetchall():
#     print(result)

# import json
# with open("userData.json", 'r') as file:
#     jsonFile = json.load(file)
#     for data in jsonFile['Users']:
#         sql = "INSERT INTO Users (username, password) VALUES ('%s', '%s')" % (data['username'], data['password'])
#         database.execute(sql)
#
#
#
# database.commit()
