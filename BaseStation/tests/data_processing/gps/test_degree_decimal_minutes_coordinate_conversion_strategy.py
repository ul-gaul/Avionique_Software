from math import isclose
from unittest import TestCase
from unittest.mock import Mock

from parameterized import parameterized

from src.data_processing.gps.degree_decimal_minutes_coordinate_conversion_strategy import \
    DegreeDecimalMinutesCoordinateConversionStrategy
from src.data_processing.gps.utm_coordinates_converter import UTMCoordinatesConverter


class DegreeDecimalMinutesCoordinateConversionStrategyTest(TestCase):
    FLOATING_POINT_PRECISION = 6
    DDM_LATITUDE = 4646.7579
    DDM_LONGITUDE = -7116.5728
    DD_LATITUDE = 46.779298
    DD_LONGITUDE = -71.276213
    EASTING = 326241
    NORTHING = 5183155

    def setUp(self):
        self.utm_coordinates_converter = Mock(spec=UTMCoordinatesConverter)
        self.conversion_strategy = DegreeDecimalMinutesCoordinateConversionStrategy(self.utm_coordinates_converter)

    def test_to_utm_should_convert_degree_decimal_minutes_to_utm(self):
        self.utm_coordinates_converter.decimal_degrees_to_utm.side_effect = self._fake_conversion

        easting, northing = self.conversion_strategy.to_utm(self.DDM_LATITUDE, self.DDM_LONGITUDE)

        self.assertEqual(easting, self.EASTING)
        self.assertEqual(northing, self.NORTHING)

    @parameterized.expand([
        ("gaul_HQ", 4646.7579, -7116.5728, 46.779298, -71.276213),
        ("spaceport_america", 3259.4167, -10658.4988, 32.990278, -106.974980),
        ("north_east_hemisphere", 4851.3968, 221.1333, 48.856613, 2.3522219),    # Paris
        ("south_west_hemisphere", -2254.4108, -4310.3738, -22.9068467, -43.1728965),  # Rio de Janeiro
        ("south_east_hemisphere", -3352.0492, 15112.4194, -33.867487, 151.206990)  # Sydney
    ])
    def test_to_decimal_degree_should_convert_from_degree_decimal_minutes(self, _, ddm_lat, ddm_long, dd_lat, dd_long):
        gps_coordinates = self.conversion_strategy.to_decimal_degrees(ddm_lat, ddm_long)

        self.assertAlmostEqual(gps_coordinates.decimal_degrees_latitude, dd_lat, self.FLOATING_POINT_PRECISION)
        self.assertAlmostEqual(gps_coordinates.decimal_degrees_longitude, dd_long, self.FLOATING_POINT_PRECISION)

    def _fake_conversion(self, latitude: float, longitude: float):  # TODO: use mockito/hamcrest for this
        if isclose(latitude, self.DD_LATITUDE, abs_tol=0.000001) and isclose(longitude, self.DD_LONGITUDE,
                                                                             abs_tol=0.000001):
            return self.EASTING, self.NORTHING
