from LoginSystems import LoginSystemManager

if __name__ == '__main__':
    loginSystem = LoginSystemManager()

    print("Select login system to run:")
    print("1: Terrible")
    print("2: Bad")
    print("3: Average")
    print("4: Good")


    mode = input()
    while (not mode.isdigit() or int(mode) > 4 or int(mode) < 0):
        mode = input()

    if mode == '1':
        loginSystem.runTerrible()
    elif mode == '2':
        loginSystem.runBad()
    elif mode == '3':
        loginSystem.runAverage()
    else:
        loginSystem.runGood()