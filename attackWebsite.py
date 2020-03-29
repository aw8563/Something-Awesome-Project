from PasswordCracker.Attacker import Attacker

# login url of website
LOGIN_URL = 'http://127.0.0.1:5000/login'
LOGOUT_URL = 'http://127.0.0.1:5000/logout'

# This will most likely only work for my website
# If for some reason you want to attack another website you will have to modify this function
def checkSuccess(response):
    return "HELLO" in response.content.decode()


if __name__ == '__main__':
    attacker = Attacker(LOGIN_URL, LOGOUT_URL, testMode=False, verbose=True)

    # set attack method parameters here if you want to
    bruteForce = attacker.getAttackMethod("BruteForceAttack")
    dictionary = attacker.getAttackMethod("DictionaryAttack")

    bruteForce.length = 4
    dictionary.length = 3

    # simple rule that adds "!" to end of pw
    def myRule(string):
        return string + "!"

    dictionary.addRule(myRule)
    dictionary.addDictionary(["hi", "world", "the", "quick", "brown"])

    # perform the attack! You can specify which attacks to use if you want
    password = attacker.runAttack(checkSuccess, "DictionaryAttack", findAll=True)
    print("\n\nPassword is <%s>" % password)