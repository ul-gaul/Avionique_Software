from unittest import TestCase

from src.data_processing.gps.decimal_degrees_coordinate_conversion_strategy import \
    DecimalDegreesCoordinateConversionStrategy
from src.data_processing.gps.gps_coordinates import GpsCoordinates


class DecimalDegreesCoordinateConversionStrategyTest(TestCase):
    LATITUDE = 46.77930
    LONGITUDE = -71.27621
    GPS_COORDINATES = GpsCoordinates(LATITUDE, LONGITUDE)

    def setUp(self):
        self.conversion_strategy = DecimalDegreesCoordinateConversionStrategy()

    def test_to_decimal_degrees_should_return_same_coordinates(self):
        gps_coordinates = self.conversion_strategy.to_decimal_degrees(self.LATITUDE, self.LONGITUDE)

        self.assertEqual(gps_coordinates.decimal_degrees_latitude, self.LATITUDE)
        self.assertEqual(gps_coordinates.decimal_degrees_longitude, self.LONGITUDE)
