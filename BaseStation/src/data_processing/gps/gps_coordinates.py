class GpsCoordinates:
    def __init__(self, decimal_degrees_latitude: float, decimal_degrees_longitude: float):
        self._decimal_degrees_latitude = decimal_degrees_latitude
        self._decimal_degrees_longitude = decimal_degrees_longitude

    @property
    def decimal_degrees_latitude(self):
        return self._decimal_degrees_latitude

    @property
    def decimal_degrees_longitude(self):
        return self._decimal_degrees_longitude

    def __eq__(self, other):
        if not isinstance(other, GpsCoordinates):
            return False

        return (self.decimal_degrees_latitude == other.decimal_degrees_latitude and
                self.decimal_degrees_longitude == other.decimal_degrees_longitude)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self._decimal_degrees_latitude, self._decimal_degrees_longitude))
