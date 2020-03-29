from LoginSystems import BadLoginSystem, AverageLoginSystem, GoodLoginSystem

class LoginSystemManager():
    def __init__(self, host='localhost', port=5000):
        self.bad = BadLoginSystem.app
        self.average = AverageLoginSystem.app
        self.good = GoodLoginSystem.app

        self.host = host
        self.port = port

    def runBad(self):
        self.bad.run(self.host, self.port)

    def runAverage(self):
        self.average.run(self.host, self.port)

    def runGood(self):
        self.good.run(self.host, self.port)

