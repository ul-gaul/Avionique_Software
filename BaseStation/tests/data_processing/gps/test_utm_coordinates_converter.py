import unittest

from src.data_processing.gps.gps_coordinates import GpsCoordinates
from src.data_processing.gps.utm_coordinates_converter import UTMCoordinatesConverter
from src.data_processing.gps.utm_zone import UTMZone


class UTMCoordinatesConverterTest(unittest.TestCase):
    """
    UTM coordinates obtained from https://www.geoplaner.com/
    """

    FLOATING_POINT_PRECISION = 0

    def test_decimal_degrees_to_utm_gaul_HQ(self):
        converter = UTMCoordinatesConverter(UTMZone.zone_19t)
        gaul_hq_coordinates = GpsCoordinates(46.779298, -71.276213)

        utm_coordinates = converter.decimal_degrees_to_utm(gaul_hq_coordinates)

        self.assertAlmostEqual(utm_coordinates.easting, 326241, self.FLOATING_POINT_PRECISION)
        self.assertAlmostEqual(utm_coordinates.northing, 5183155, self.FLOATING_POINT_PRECISION)

    def test_decimal_degrees_to_utm_spaceport_america(self):
        converter = UTMCoordinatesConverter(UTMZone.zone_13S)
        spaceport_america_coordinates = GpsCoordinates(32.990278, -106.974980)

        utm_coordinates = converter.decimal_degrees_to_utm(spaceport_america_coordinates)

        self.assertAlmostEqual(utm_coordinates.easting, 315470, self.FLOATING_POINT_PRECISION)
        self.assertAlmostEqual(utm_coordinates.northing, 3651941, self.FLOATING_POINT_PRECISION)
