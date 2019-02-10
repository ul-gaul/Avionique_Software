from pyproj import Proj

from src.data_processing.utm_zone import UTMZone


class GeoCoordinateConverter:

    def __init__(self, utm_zone: UTMZone):
        self.converter = Proj("+proj=utm +zone={0}, +north +ellps=WGS84 +datum=WGS84 +units=m +no_defs"
                              .format(utm_zone.value))

    def from_long_lat_to_utm(self, longitude, latitude):
        return self.converter(longitude, latitude)
