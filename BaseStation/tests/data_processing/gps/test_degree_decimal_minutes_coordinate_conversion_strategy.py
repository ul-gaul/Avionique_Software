from math import isclose
from unittest import TestCase
from unittest.mock import Mock

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

    def test_degree_decimal_minute_to_decimal_degree_gaul_HQ(self):
        latitude, longitude = self.conversion_strategy.degree_decimal_minutes_to_decimal_degrees(4646.7579, -7116.5728)

        self.assertAlmostEqual(latitude, 46.779298, self.FLOATING_POINT_PRECISION)
        self.assertAlmostEqual(longitude, -71.276213, self.FLOATING_POINT_PRECISION)

    def test_degree_decimal_minute_to_decimal_degree_spaceport_america(self):
        latitude, longitude = self.conversion_strategy.degree_decimal_minutes_to_decimal_degrees(3259.4167, -10658.4988)

        self.assertAlmostEqual(latitude, 32.990278, self.FLOATING_POINT_PRECISION)
        self.assertAlmostEqual(longitude, -106.974980, self.FLOATING_POINT_PRECISION)

    def test_degree_decimal_minute_to_decimal_degree_north_east_hemisphere(self):
        # Paris
        latitude, longitude = self.conversion_strategy.degree_decimal_minutes_to_decimal_degrees(4851.3968, 221.1333)

        self.assertAlmostEqual(latitude, 48.856613, self.FLOATING_POINT_PRECISION)
        self.assertAlmostEqual(longitude, 2.3522219, self.FLOATING_POINT_PRECISION)

    def test_degree_decimal_minute_to_decimal_degree_south_west_hemisphere(self):
        # Rio de Janeiro
        latitude, longitude = self.conversion_strategy.degree_decimal_minutes_to_decimal_degrees(-2254.4108, -4310.3738)

        self.assertAlmostEqual(latitude, -22.9068467, self.FLOATING_POINT_PRECISION)
        self.assertAlmostEqual(longitude, -43.1728965, self.FLOATING_POINT_PRECISION)

    def test_degree_decimal_minute_to_decimal_degree_south_east_hemisphere(self):
        # Sydney
        latitude, longitude = self.conversion_strategy.degree_decimal_minutes_to_decimal_degrees(-3352.0492, 15112.4194)

        self.assertAlmostEqual(latitude, -33.867487, self.FLOATING_POINT_PRECISION)
        self.assertAlmostEqual(longitude, 151.206990, self.FLOATING_POINT_PRECISION)

    def _fake_conversion(self, latitude: float, longitude: float):  # TODO: use mockito/hamcrest for this
        if isclose(latitude, self.DD_LATITUDE, abs_tol=0.000001) and isclose(longitude, self.DD_LONGITUDE,
                                                                             abs_tol=0.000001):
            return self.EASTING, self.NORTHING
