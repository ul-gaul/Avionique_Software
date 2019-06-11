from typing import Tuple

from src.data_processing.gps.coordinate_conversion_strategy import CoordinateConversionStrategy


class DecimalDegreesCoordinateConversionStrategy(CoordinateConversionStrategy):

    def to_utm(self, latitude: float, longitude: float) -> Tuple[float, float]:
        return self.utm_coordinates_converter.decimal_degrees_to_utm(latitude, longitude)
