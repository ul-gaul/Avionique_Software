import abc
from typing import Tuple

from src.data_processing.gps.gps_coordinates import GpsCoordinates
from src.data_processing.gps.utm_coordinates_converter import UTMCoordinatesConverter


class CoordinateConversionStrategy:
    __metaclass__ = abc.ABCMeta

    def __init__(self, utm_coordinates_converter: UTMCoordinatesConverter):
        self.utm_coordinates_converter = utm_coordinates_converter

    @abc.abstractmethod
    def to_utm(self, latitude: float, longitude: float) -> Tuple[float, float]:  # TODO: accept GpsCoordinates as input?
        pass

    @abc.abstractmethod
    def to_decimal_degrees(self, latitude: float, longitude: float) -> GpsCoordinates:
        pass
