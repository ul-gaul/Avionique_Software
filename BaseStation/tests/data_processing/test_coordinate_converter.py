import unittest

from src.data_processing.coordinate_converter import CoordinateConverter


class CoordinateConverterTest(unittest.TestCase):
    """
    UTM coordinates obtained from https://www.geoplaner.com/
    """

    FLOATING_POINT_PRECISION = 6

    def setUp(self):
        pass

    def test_degree_decimal_minute_to_decimal_degree_gaul_HQ(self):
        latitude, longitude = CoordinateConverter.degree_decimal_minute_to_decimal_degree(4646.7579, -7116.5728)

        self.assertAlmostEqual(latitude, 46.779298, self.FLOATING_POINT_PRECISION)
        self.assertAlmostEqual(longitude, -71.276213, self.FLOATING_POINT_PRECISION)

    def test_degree_decimal_minute_to_decimal_degree_spaceport_america(self):
        latitude, longitude = CoordinateConverter.degree_decimal_minute_to_decimal_degree(3259.4167, -10658.4988)

        self.assertAlmostEqual(latitude, 32.990278, self.FLOATING_POINT_PRECISION)
        self.assertAlmostEqual(longitude, -106.974980, self.FLOATING_POINT_PRECISION)

    def test_degree_decimal_minute_to_decimal_degree_north_east_hemisphere(self):
        # Paris
        latitude, longitude = CoordinateConverter.degree_decimal_minute_to_decimal_degree(4851.3968, 221.1333)

        self.assertAlmostEqual(latitude, 48.856613, self.FLOATING_POINT_PRECISION)
        self.assertAlmostEqual(longitude, 2.3522219, self.FLOATING_POINT_PRECISION)

    def test_degree_decimal_minute_to_decimal_degree_south_west_hemisphere(self):
        # Rio de Janeiro
        latitude, longitude = CoordinateConverter.degree_decimal_minute_to_decimal_degree(-2254.4108, -4310.3738)

        self.assertAlmostEqual(latitude, -22.9068467, self.FLOATING_POINT_PRECISION)
        self.assertAlmostEqual(longitude, -43.1728965, self.FLOATING_POINT_PRECISION)

    def test_degree_decimal_minute_to_decimal_degree_south_east_hemisphere(self):
        # Sydney
        latitude, longitude = CoordinateConverter.degree_decimal_minute_to_decimal_degree(-3352.0492, 15112.4194)

        self.assertAlmostEqual(latitude, -33.867487, self.FLOATING_POINT_PRECISION)
        self.assertAlmostEqual(longitude, 151.206990, self.FLOATING_POINT_PRECISION)
