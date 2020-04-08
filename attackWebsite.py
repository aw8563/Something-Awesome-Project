from PasswordCracker.PasswordCracker import Attacker

# login url of website
LOGIN_URL = 'http://127.0.0.1:5000/login'
LOGOUT_URL = 'http://127.0.0.1:5000/logout'

# top 10000 english words
DICTIONARY_PATH = "PasswordCracker/dictionary.txt"

# This will most likely only work for my website
# If for some reason you want to attack another website you will have to modify this function
def checkSuccess(response):
    return "HELLO" in response.content.decode()

if __name__ == '__main__':
    attacker = Attacker(LOGIN_URL, LOGOUT_URL)

    # set attack method parameters here if you want to
    bruteForce = attacker.getAttackMethod("BruteForceAttack")
    dictionary = attacker.getAttackMethod("DictionaryAttack")

    bruteForce.length = 5
    dictionary.length = 2

    # simple rule that adds "123" to end of pw
    def myRule(string):
        return string + "123"

    # list of top 10,000 common english words. This includes swear words and names.
    with open(DICTIONARY_PATH, 'r') as file:
        # remove the newline from word and add to list
        wordList = [word[:-1] for word in file]

    dictionary.addRule(myRule)
    dictionary.addWords(wordList)

    # perform the attack! You can specify which attacks to use if you want
    attacker.runAttack(checkSuccess, ["DictionaryAttack"],findAll=True, testMode=True, verbose=False, log=False)