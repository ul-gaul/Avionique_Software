from typing import Tuple

from src.data_processing.gps.coordinate_conversion_strategy import CoordinateConversionStrategy


class DegreeDecimalMinutesCoordinateConversionStrategy(CoordinateConversionStrategy):
    def to_utm(self, latitude: float, longitude: float) -> Tuple[float, float]:
        dd_lat, dd_long = self.degree_decimal_minutes_to_decimal_degrees(latitude, longitude)

        return self.utm_coordinates_converter.decimal_degrees_to_utm(dd_lat, dd_long)

    @staticmethod
    def degree_decimal_minutes_to_decimal_degrees(latitude: float, longitude: float) -> Tuple[float, float]:
        """
        Converts coordinates in format DDMM.MMMM to DD.DDDD
        """
        dd_lat = DegreeDecimalMinutesCoordinateConversionStrategy._ddmm2dd(latitude)
        dd_lon = DegreeDecimalMinutesCoordinateConversionStrategy._ddmm2dd(longitude)

        return dd_lat, dd_lon

    @staticmethod
    def _ddmm2dd(coordinate: float):
        degrees = int(coordinate / 100)
        minutes = coordinate - (degrees * 100)
        return degrees + (minutes / 60)
