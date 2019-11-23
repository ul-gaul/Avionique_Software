class Apogee:
    def __init__(self, timestamp: float, altitude: float):
        self._timestamp = timestamp
        self._altitude = altitude
        self._is_reached = True

    @property
    def timestamp(self) -> float:
        return self._timestamp

    @property
    def altitude(self) -> float:
        return self._altitude

    @property
    def is_reached(self) -> bool:
        return self._is_reached

    @staticmethod
    def unreached():
        apogee = Apogee(0, 0)
        apogee._is_reached = False

        return apogee

    def __eq__(self, other):
        if not isinstance(other, Apogee):
            return False

        return (self._timestamp == other.timestamp and self._altitude == other.altitude and
                self._is_reached == other.is_reached)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self._timestamp, self._altitude, self._is_reached))
