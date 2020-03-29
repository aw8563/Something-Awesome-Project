from PasswordCracker.Attacker import Attacker

# login url of website
WEBSITE_URL = 'http://127.0.0.1:5000/login'

# This will only work for my website
# If for some reason you want to attack another website you will have to modify this function
def checkSuccess(response):
    return "HELLO" in response.content.decode()


if __name__ == '__main__':
    attacker = Attacker(WEBSITE_URL)

    # set attack method parameters here if you want to
    attacker.getAttackMethod("BruteForceAttack").length = 5


    password = attacker.runAttack(checkSuccess)

    print("\n\nPassword is <%s>" % password)