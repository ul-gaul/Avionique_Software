from src.data_processing.gps.coordinate_conversion_strategy import CoordinateConversionStrategy
from src.data_processing.gps.gps_coordinates import GpsCoordinates


class DegreeDecimalMinutesCoordinateConversionStrategy(CoordinateConversionStrategy):
    def to_decimal_degrees(self, latitude: float, longitude: float) -> GpsCoordinates:
        """
        Converts coordinates in format DDMM.MMMM to DD.DDDD
        """
        dd_lat = DegreeDecimalMinutesCoordinateConversionStrategy._ddmm2dd(latitude)
        dd_lon = DegreeDecimalMinutesCoordinateConversionStrategy._ddmm2dd(longitude)

        return GpsCoordinates(dd_lat, dd_lon)

    @staticmethod
    def _ddmm2dd(coordinate: float):
        degrees = int(coordinate / 100)
        minutes = coordinate - (degrees * 100)
        return degrees + (minutes / 60)
