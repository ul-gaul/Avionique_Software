class ApogeeCalculator:
    def __init__(self):
        self.points = []
        self.draw_apogee = False
        self.apogee = 0
        self.apogee_index = None

        self.last_altitude = 0
        self.last_altitude_index = 0

    def update(self, values: list): #Faire des test unitaires>
        length = len(values)
        if length > 0:
            if self.apogee != 0 or self.last_altitude_index == 0 or ((length-1) - self.last_altitude_index) < 0:
                #if (values[-1] - self.last_altitude) < 0:
                for i in range(self.last_altitude_index, length-1):
                    if values[i] > self.apogee:
                        if values[i] - values[i + 1] >= 0:
                            self.apogee = values[i]
                            self.apogee_index = i
                            self.draw_apogee = True
            else:
                self.set_value_none()

            self.last_altitude = values[-1]
            self.last_altitude_index = length - 1
        else:
            self.set_value_none()

    def set_value_none(self):
        self.apogee = 0
        self.apogee_index = None
        self.draw_apogee = False

    def reset(self):
        self.points = []
        self.draw_apogee = False
        self.apogee = None
        self.apogee_index = None

        self.last_altitude = 0
        self.last_altitude_index = 0

    def has_apogee(self):
        return self.apogee is not 0

