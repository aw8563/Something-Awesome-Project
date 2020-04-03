from flask_login import UserMixin, login_user
import hashlib
import sqlite3

DATABASE_PATH = "LoginSystems/GoodLoginSystem/database.db"
class User(UserMixin):
    def __init__(self, id, username, passwordHash):
        self.id = id
        self.username = username
        self.passwordHash = passwordHash

    def get_id(self):
        return self.id

    def __str__(self):
        return "ID: %d | Username: %s" %(self.id, self.username)


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
        hash = hashlib.sha256()
        hash.update(password.encode('utf-8'))

        hashedPassword = hash.hexdigest()
        result = self.database.execute("select * from Users where username = '%s' and password = '%s' limit 1" %
                                       (username, hashedPassword)).fetchone()

        if result:
            login_user(User(result[0], result[1], result[2]))
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


database = sqlite3.connect("database.db")


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
