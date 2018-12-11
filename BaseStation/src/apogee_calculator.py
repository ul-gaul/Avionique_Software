class ApogeeCalculator:
    def __init__(self):
        self.apogee = 0
        self.apogee_index = 0

        self.last_altitude = 0
        self.last_altitude_index = 0

    def update(self, values: list):
        length = len(values)

        if length == 0 or length < self.apogee_index:
            self.set_value_none()
            return

        if length == self.last_altitude_index:
            return

        if self.apogee_index < length or self.last_altitude_index == 0 or (self.last_altitude_index - values[-1]) <= 0 or self.apogee == 0:
            for i in range(self.last_altitude_index, length-1):
                if values[i] >= self.apogee:
                    if (values[i] - values[i + 1]) >= 0:
                        self.apogee = values[i]
                        self.apogee_index = i
        else:
            self.set_value_none()

        self.last_altitude = values[-1]
        self.last_altitude_index = length-1

    def set_value_none(self):
        self.apogee = 0
        self.apogee_index = 0

    def reset(self):
        self.apogee = 0
        self.apogee_index = 0

        self.last_altitude = 0
        self.last_altitude_index = None

    def has_apogee(self):
        return self.apogee_index is not 0
