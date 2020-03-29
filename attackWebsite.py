from PasswordCracker.Attacker import Attacker

# login url of website
WEBSITE_URL = 'http://127.0.0.1:5000/login'
USERNAME = 'hello'

# This will only work for my website
# If for some reason you want to attack another website you will have to modify this function
def checkSuccess(response):
    return "HELLO" in response.content.decode()


if __name__ == '__main__':
    attacker = Attacker(WEBSITE_URL, USERNAME, testMode=True, verbose=True)

    # set attack method parameters here if you want to
    bruteForce = attacker.getAttackMethod("BruteForceAttack")
    dictionary = attacker.getAttackMethod("DictionaryAttack")

    bruteForce.length = 4
    dictionary.length = 3

    def myRule(string):
        return string + "2"

    dictionary.addRule(myRule)
    dictionary.addDictionary(["hello", "world", "the", "quick", "brown"])

    # perform the attack! You can specify which attacks to use if you want
    password = attacker.runAttack(checkSuccess, "DictionaryAttack")
    print("\n\nPassword is <%s>" % password)