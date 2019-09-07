from pyproj import Proj

from src.data_processing.gps.gps_coordinates import GpsCoordinates
from src.data_processing.gps.utm_coordinates import UTMCoordinates
from src.data_processing.gps.utm_zone import UTMZone


class UTMCoordinatesConverter:
    def __init__(self, utm_zone: UTMZone):
        self.converter = Proj("+proj=utm +zone={0}, +north +ellps=WGS84 +datum=WGS84 +units=m +no_defs"
                              .format(utm_zone.value))

    def decimal_degrees_to_utm(self, gps_coordinates: GpsCoordinates) -> UTMCoordinates:
        """
        Converts coordinates in format DD.DDDD to UTM
        :return: easting, northing
        """
        easting, northing = self.converter(gps_coordinates.decimal_degrees_longitude,
                                           gps_coordinates.decimal_degrees_latitude)
        return UTMCoordinates(easting, northing)
