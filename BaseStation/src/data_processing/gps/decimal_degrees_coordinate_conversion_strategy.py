from typing import Tuple

from src.data_processing.gps.coordinate_conversion_strategy import CoordinateConversionStrategy
from src.data_processing.gps.gps_coordinates import GpsCoordinates


class DecimalDegreesCoordinateConversionStrategy(CoordinateConversionStrategy):

    def to_utm(self, latitude: float, longitude: float) -> Tuple[float, float]:
        return self.utm_coordinates_converter.decimal_degrees_to_utm(latitude, longitude)

    def to_decimal_degrees(self, latitude: float, longitude: float) -> GpsCoordinates:
        return GpsCoordinates(latitude, longitude)
