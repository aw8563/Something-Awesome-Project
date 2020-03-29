from abc import ABC, abstractmethod
import itertools
import more_itertools


class Attack(ABC):
    def __init__(self, length):
        self.length = length

    @abstractmethod
    def generatePasswords(self):
        pass

    def __str__(self):
        return type(self).__name__

class BruteForceAttack(Attack):
    def __init__(self, length=8, hasCapitals=False, hasSpecialChars=False):
        super().__init__(length) # length of password

        self.hasCapitals = hasCapitals # does pw contain capitals
        self.hasSpecialChars = hasSpecialChars # does pw contain special characters

    # returns generator for passwords
    def generatePasswords(self):

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
        for length in range(self.length):
            # There are faster methods but this way allows us to return result as a generator which is important
            for combination in itertools.combinations_with_replacement(chars, length + 1):
                for permutation in more_itertools.distinct_permutations(combination):
                    # yield is basical ly the same as return except it happens each iteration
                    # this means we can try each password as we are iterating
                    # this is much than waiting for the entire list to generate and looping through it again
                    yield "".join(permutation)

    def __str__(self):
        return super().__str__() + " | Max Length: %s, %s, %s" %(self.length, \
                                    "Capitals" if self.hasCapitals else "No Capitals", \
                                    "Special Characters" if self.hasSpecialChars else "No Special Characters")


class DictionaryAttack(Attack):
    def __init__(self, length=3, words=[], rules = []):
        super().__init__(length) # how many words are included. Eg a length 2 password could be "helloworld"

        # list of words to include
        self.words = words

        # rules that modify a word. Eg a rule might capitalize the first letter of a word
        self.rules = [self.doNothingRule, self.capitaliseRule, self.addOneToEndRule] + rules

    # returns generator for passwords
    def generatePasswords(self):
        for length in range(self.length):
            for rule in self.rules:
                for combination in itertools.combinations(self.words, length + 1):
                    for permutation in itertools.permutations(combination):

                        # yield is basically the same as return except it happens each iteration
                        # this means we can try each password as we are iterating
                        # this is much than waiting for the entire list to generate and looping through it again
                        yield rule("".join(permutation))

    # base rule that does nothing
    def doNothingRule(self, string):
        return string

    # simple rule that capitalises first char
    def capitaliseRule(self, string):
        return string[0].upper() + string[1:]

    # simple rule that adds '1' to end of string
    def addOneToEndRule(self, string):
        return string + "1"

    # add new rule
    def addRule(self, rule):
        self.rules.append(rule)

    def addDictionary(self, words):
        self.words += words

    def __str__(self):
        return super().__str__() + " | Max number of words: %s, Number of rules: %s" \
                                    % (self.length, len(self.rules) - 1)