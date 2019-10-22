from unittest import TestCase

from parameterized import parameterized

from src.data_processing.gps.degree_decimal_minutes_coordinate_conversion_strategy import \
    DegreeDecimalMinutesCoordinateConversionStrategy


class DegreeDecimalMinutesCoordinateConversionStrategyTest(TestCase):
    FLOATING_POINT_PRECISION = 6

    def setUp(self):
        self.conversion_strategy = DegreeDecimalMinutesCoordinateConversionStrategy()

    @parameterized.expand([
        ("gaul_HQ", 4646.7579, -7116.5728, 46.779298, -71.276213),
        ("spaceport_america", 3259.4167, -10658.4988, 32.990278, -106.974980),
        ("north_east_hemisphere", 4851.3968, 221.1333, 48.856613, 2.3522219),  # Paris
        ("south_west_hemisphere", -2254.4108, -4310.3738, -22.9068467, -43.1728965),  # Rio de Janeiro
        ("south_east_hemisphere", -3352.0492, 15112.4194, -33.867487, 151.206990)  # Sydney
    ])
    def test_to_decimal_degree_should_convert_from_degree_decimal_minutes(self, _, ddm_lat, ddm_long, dd_lat, dd_long):
        gps_coordinates = self.conversion_strategy.to_decimal_degrees(ddm_lat, ddm_long)

        self.assertAlmostEqual(gps_coordinates.decimal_degrees_latitude, dd_lat, self.FLOATING_POINT_PRECISION)
        self.assertAlmostEqual(gps_coordinates.decimal_degrees_longitude, dd_long, self.FLOATING_POINT_PRECISION)
