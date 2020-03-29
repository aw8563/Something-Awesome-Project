from LoginSystems import BadLoginSystem, AverageLoginSystem, GoodLoginSystem

class LoginSystemManager():
    def __init__(self):
        self.bad = BadLoginSystem.app
        self.average = AverageLoginSystem.app
        self.good = GoodLoginSystem.app

    def runBad(self):
        self.bad.run()

    def runAverage(self):
        self.average.run()

    def runGood(self):
        self.good.run()

