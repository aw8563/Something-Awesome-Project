from abc import ABC, abstractmethod
import itertools
import more_itertools


class PasswordAttack(ABC):
    def __init__(self, length):
        self.length = length

    @abstractmethod
    def generatePasswords(self):
        pass

    def __str__(self):
        return type(self).__name__

class BruteForceAttack(PasswordAttack):
    def __init__(self, length=8, hasCapitals=False, hasSpecialChars=False):
        super().__init__(length) # length of password

        self.hasCapitals = hasCapitals # does pw contain capitals
        self.hasSpecialChars = hasSpecialChars # does pw contain special characters


    # returns list of passwords
    def generatePasswords(self):
        result = []

        # normal characters
        chars = "abcdefghijklmnopqrstuvwxyz"

        # numbers
        chars += "0123456789"

        # capitals
        if self.hasCapitals:
            chars += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        # special characters
        if self.hasSpecialChars:
            chars += "!@#$%^&*()-_=+[]{},./<>?;:"

        for combination in itertools.combinations_with_replacement(chars, self.length):
            for permutation in more_itertools.distinct_permutations(combination):
                yield "".join(permutation)

    def __str__(self):
        return super().__str__() + " | Max Length: %s, %s, %s" %(self.length, \
                                    "Capitals" if self.hasCapitals else "No Capitals", \
                                    "Special Characters" if self.hasSpecialChars else "No Special Characters")


class DictionaryAttack(PasswordAttack):
    def __init__(self, length=3, words=[], rules=[]):
        super().__init__(length) # how many words are included. Eg a length 2 password could be "helloworld"

        self.words = words # list of words to include
        self.rules = rules # rules that modify a word. Eg a rule might capitalize the first letter of a word

    # returns list of passwords
    def generatePasswords(self):
        return ["dictionary", "attack", "pws"]

    def __str__(self):
        return super().__str__() + " | Max number of words: %s, Number of rules: %s" % (self.length, len(self.rules))