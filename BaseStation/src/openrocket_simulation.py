from src.domain_error import DomainError


class OpenRocketSimulation:
    def __init__(self, filename):
        self.time = []
        self.altitude = []

        try:
            with open(filename) as file:
                datatemp = file.read().splitlines()

            for dat in datatemp:
                data = dat.split(",")
                self.time.append(float(data[0]))
                self.altitude.append(float(data[1]))
        except ValueError:

            raise DomainError("Le fichier de simulation " + filename + " n'a pas pu être chargé")