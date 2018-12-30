class ApogeeCalculator:
    def __init__(self):
        self.apogee = 0
        self.apogee_index = 0

        self.last_altitude = 0
        self.last_altitude_index = 0

    def update(self, values: list):
        length = len(values)

        if length < 2 or length < self.apogee_index:
            self.set_value_none()
            return

        if length == self.last_altitude_index:
            return

        if self.check_change_apogee(length):
            for i in range(self.last_altitude_index, length-1):
                if values[i] > 0 and values[i] >= self.apogee:
                    if (values[i] - values[i + 1]) >= 0:
                        self.apogee = values[i]
                        self.apogee_index = i
        else:
            self.set_value_none()

        self.last_altitude = values[length-2]
        self.last_altitude_index = length-1

    def check_change_apogee(self, length : int):
        return self.apogee_index < length or self.last_altitude_index == 0 or self.apogee == 0

    def set_value_none(self):
        self.apogee = 0
        self.apogee_index = 0

    def reset(self):
        self.apogee = 0
        self.apogee_index = 0

        self.last_altitude = 0
        self.last_altitude_index = None

    def get_apogee(self):
        if self.apogee_index is not 0:
            rep = (self.apogee_index, self.apogee)
            return rep

        return None
