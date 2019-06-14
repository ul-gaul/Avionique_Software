import unittest

from src.data_processing.gps.utm_coordinates_converter import UTMCoordinatesConverter
from src.data_processing.gps.utm_zone import UTMZone


class UTMCoordinatesConverterTest(unittest.TestCase):
    """
    UTM coordinates obtained from https://www.geoplaner.com/
    """

    FLOATING_POINT_PRECISION = 0

    def test_decimal_degrees_to_utm_gaul_HQ(self):
        converter = UTMCoordinatesConverter(UTMZone.zone_19t)

        easting, northing = converter.decimal_degrees_to_utm(46.779298, -71.276213)

        self.assertAlmostEqual(easting, 326241, self.FLOATING_POINT_PRECISION)
        self.assertAlmostEqual(northing, 5183155, self.FLOATING_POINT_PRECISION)

    def test_decimal_degrees_to_utm_spaceport_america(self):
        converter = UTMCoordinatesConverter(UTMZone.zone_13S)

        easting, northing = converter.decimal_degrees_to_utm(32.990278, -106.974980)

        self.assertAlmostEqual(easting, 315470, self.FLOATING_POINT_PRECISION)
        self.assertAlmostEqual(northing, 3651941, self.FLOATING_POINT_PRECISION)
