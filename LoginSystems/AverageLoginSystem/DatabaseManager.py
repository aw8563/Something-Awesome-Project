from flask_login import UserMixin, login_user
import sqlite3

DATABASE_PATH = "LoginSystems/AverageLoginSystem/database.db"
class User(UserMixin):
    def __init__(self, id):
        self.id = id


    def get_id(self):
        return self.id

    def __str__(self):
        return "Account_%d" %(self.id)

class DatabaseManager():
    def __init__(self):
        self.database = sqlite3.connect(DATABASE_PATH, check_same_thread=False)

    def getUser(self, id):
        result = self.database.execute("select id from Users where id = %d" % id).fetchone()

        if (result):
            return User(result[0])


    def addUser(self, username, password):
        if self.database.execute("select * from Users where username ='%s' limit 1" % username).fetchone():
            return "Username in use"

        if not self.checkPassword(password):
            return "Password too weak"


        self.database.execute("insert into Users (username, password) values('%s', '%s')" % (username, password))
        self.database.commit()

        result = self.database.execute("select id from Users where username = '%s'" %username).fetchone()

        return User(result[0])

    def checkPassword(self, password):
        return len(password) > 6

    def loginUser(self, username, password):
        result = self.database.execute("select * from Users where username = '%s' and password = '%s' limit 1" %
                                       (username, password)).fetchone()

        if result:
            login_user(User(result[0]))
            return True

        return False

    def query(self, value):
        try:
            sql = "select * from Items where name like '%s' or id = %s" % ('%'+value+'%', value if value.isdigit() else -1)
            result = self.database.execute(sql).fetchall()
        except Exception as e:
            print("BAD SQL QUERY\n", sql, "\n", e)
            return []

        return result or []