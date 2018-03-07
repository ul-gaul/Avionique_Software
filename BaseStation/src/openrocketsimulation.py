
class OpenRocketSimulation:
    def __init__(self, filename):
        self.time = []
        self.altitude = []

        with open(filename) as file:
            datatemp = file.read().splitlines()

        for dat in datatemp:
            data = dat.split(",")
            self.time.append(float(data[0]))
            self.altitude.append(float(data[1]))