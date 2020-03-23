from LoginSystems import TerribleLoginSystem, BadLoginSystem, AverageLoginSystem, GoodLoginSystem

class LoginSystemManager():
    def __init__(self):
        self.terrible = TerribleLoginSystem.app
        self.bad = BadLoginSystem.app
        self.average = AverageLoginSystem.app
        self.good = GoodLoginSystem.app

    def runBad(self):
        self.bad.run()

    def runTerrible(self):
        self.terrible.run()

    def runAverage(self):
        self.average.run()

    def runGood(self):
        self.good.run()

