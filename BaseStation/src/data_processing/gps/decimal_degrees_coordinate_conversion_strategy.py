from src.data_processing.gps.coordinate_conversion_strategy import CoordinateConversionStrategy
from src.data_processing.gps.gps_coordinates import GpsCoordinates


class DecimalDegreesCoordinateConversionStrategy(CoordinateConversionStrategy):
    def to_decimal_degrees(self, latitude: float, longitude: float) -> GpsCoordinates:
        return GpsCoordinates(latitude, longitude)
