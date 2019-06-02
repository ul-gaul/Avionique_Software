from typing import Tuple

from pyproj import Proj

from src.data_processing.utm_zone import UTMZone


class CoordinateConverter:

    def __init__(self, utm_zone: UTMZone):
        self.converter = Proj("+proj=utm +zone={0}, +north +ellps=WGS84 +datum=WGS84 +units=m +no_defs"
                              .format(utm_zone.value))

    def from_long_lat_to_utm(self, latitude: float, longitude: float):
        return self.converter(longitude, latitude)

    @staticmethod
    def degree_decimal_minute_to_decimal_degree(latitude: float, longitude: float) -> Tuple[float, float]:
        """
        Converts coordinates in format DDMM.MMMM to DD.DDDD
        """
        dd_lat = CoordinateConverter._ddmm2dd(latitude)
        dd_lon = CoordinateConverter._ddmm2dd(longitude)

        return dd_lat, dd_lon

    @staticmethod
    def _ddmm2dd(coordinate: float):
        degrees = int(coordinate / 100)
        minutes = coordinate - (degrees * 100)
        return degrees + (minutes / 60)
