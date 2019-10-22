class UTMCoordinates:
    def __init__(self, easting: float, northing: float):
        self._easting = easting
        self._northing = northing

    @property
    def easting(self):
        return self._easting

    @property
    def northing(self):
        return self._northing

    def __add__(self, other):
        if not isinstance(other, UTMCoordinates):
            raise TypeError("UTMCoordinates does not support addition with operand of type: " + str(type(other)))

        return UTMCoordinates(self._easting + other.easting, self._northing + other.northing)

    def __sub__(self, other):
        if not isinstance(other, UTMCoordinates):
            raise TypeError("UTMCoordinates does not support subtraction with operand of type: " + str(type(other)))

        return UTMCoordinates(self._easting - other.easting, self._northing - other.northing)

    def __truediv__(self, other):
        if not isinstance(other, (int, float)):
            raise TypeError("UTMCoordinates does not support division with operand of type: " + str(type(other)))

        return UTMCoordinates(self._easting / other, self._northing / other)

    def __eq__(self, other):
        if not isinstance(other, UTMCoordinates):
            return False

        return self._easting == other.easting and self._northing == other.northing

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self._easting, self._northing))
