from LoginSystems import LoginSystemManager

if __name__ == '__main__':
    loginSystem = LoginSystemManager()

    print("Select login system to run:")
    print("1: Bad")
    print("2: Average")
    print("3: Good")


    mode = input()
    while (not mode.isdigit() or int(mode) > 3 or int(mode) < 0):
        mode = input()

    if mode == '1':
        loginSystem.runBad()
    elif mode == '2':
        loginSystem.runAverage()
    else:
        loginSystem.runGood()