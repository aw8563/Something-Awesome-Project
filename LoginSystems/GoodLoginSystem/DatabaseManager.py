from flask_login import UserMixin, login_user
import hashlib
import sqlite3

DATABASE_PATH = "LoginSystems/GoodLoginSystem/database.db"
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
        result = self.database.execute("select * from Users where id = %d" % id).fetchone()

        if (result):
            return User(result[0])


    def addUser(self, username, password):
        if self.database.execute("select * from Users where username ='%s' limit 1" % username).fetchone():
            return "Username in use"

        if not self.checkPassword(password):
            return "Password too weak"

        self.database.execute("insert into Users (username, password) values('%s', '%s')" % (username, password))
        self.database.commit()

        result = self.database.execute("select * from Users where username = '%s'" %username).fetchone()

        return User(result[0])

    def checkPassword(self, password):
        hasLetter = False
        hasUpperCase = False
        hasDigit = False
        hasSpecialChar = False

        for c in password:
            if c.isalpha():
                hasLetter = True

            if c.isupper():
                hasUpperCase = True

            if c.isdigit():
                hasDigit = True

            if c in "!@#$%^&*()_+-=?":
                hasSpecialChar = True

        # password must be at least length 8 and contain a lowercase letter, uppercase letter, digit and special char
        return hasLetter and hasUpperCase and hasDigit and hasSpecialChar and len(password) >= 8

    def loginUser(self, username, password):
        hash = hashlib.sha256()
        hash.update(password.encode('utf-8'))

        hashedPassword = hash.hexdigest()
        result = self.database.execute("select * from Users where username = '%s' and password = '%s' limit 1" %
                                       (username, hashedPassword)).fetchone()

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


# database.execute("CREATE TABLE USERS(id INTEGER PRIMARY KEY AUTOINCREMENT , username varchar(64), password varchar(64))")
# database.execute("CREATE TABLE ITEMS(id INTEGER PRIMARY KEY AUTOINCREMENT, name varchar(64))")
#
# for result in database.execute("select * from Users").fetchall():
#     print(result)


# with open("../BadLoginSystem/userData.json", 'r') as file:
#     jsonFile = json.load(file)
#     for data in jsonFile['Users']:
#
#         username = data['username']
#         password = data['password']
#         hash = hashlib.sha256()
#         hash.update(bytes(password, 'utf-8'))
#         passwordHash = hash.hexdigest()

        # sql = "INSERT INTO Users (username, password) VALUES ('%s', '%s')" % (username, str(passwordHash))
        # database.execute(sql)





# database.commit()
