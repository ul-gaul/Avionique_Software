from typing import Tuple

from pyproj import Proj

from src.data_processing.gps.utm_zone import UTMZone


class UTMCoordinatesConverter:
    def __init__(self, utm_zone: UTMZone):
        self.converter = Proj("+proj=utm +zone={0}, +north +ellps=WGS84 +datum=WGS84 +units=m +no_defs"
                              .format(utm_zone.value))

    def decimal_degrees_to_utm(self, latitude: float, longitude: float) -> Tuple[float, float]:
        """
        Converts coordinates in format DD.DDDD to UTM
        :return: easting, northing
        """
        return self.converter(longitude, latitude)
