import abc

from src.data_processing.gps.gps_coordinates import GpsCoordinates


class CoordinateConversionStrategy:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def to_decimal_degrees(self, latitude: float, longitude: float) -> GpsCoordinates:
        pass
