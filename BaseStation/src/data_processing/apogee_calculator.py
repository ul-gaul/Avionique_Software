from src.data_processing.apogee import Apogee


class ApogeeCalculator:
    def __init__(self):
        self.apogee = Apogee.unreached()
        self.apogee_index = 0

        self.last_altitude_index = 0

    def update(self, timestamps: list, altitudes: list):
        length = len(altitudes)

        if length < 2 or length < self.apogee_index:
            self.set_value_none()
            return

        if length == self.last_altitude_index:
            return

        if self.check_change_apogee(length):
            for i in range(self.last_altitude_index, length-1):
                if altitudes[i] > 0 and altitudes[i] >= self.apogee.altitude:
                    if (altitudes[i] - altitudes[i + 1]) >= 0:
                        self.apogee = Apogee(timestamps[i], altitudes[i])
                        self.apogee_index = i
        else:
            self.set_value_none()

        self.last_altitude_index = length-1

    def check_change_apogee(self, length: int):
        return self.apogee_index < length or self.last_altitude_index == 0 or self.apogee.altitude == 0

    def set_value_none(self):
        self.apogee = Apogee.unreached()
        self.apogee_index = 0

    def reset(self):
        self.set_value_none()

        self.last_altitude_index = 0

    def get_apogee(self):
        return self.apogee
