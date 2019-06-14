from unittest import TestCase
from unittest.mock import Mock

from src.data_processing.gps.utm_coordinates_converter import UTMCoordinatesConverter
from src.data_processing.gps.decimal_degrees_coordinate_conversion_strategy import \
    DecimalDegreesCoordinateConversionStrategy


class DecimalDegreesCoordinateConversionStrategyTest(TestCase):
    LATITUDE = 46.77930
    LONGITUDE = -71.27621
    EASTING = 326241
    NORTHING = 5183155

    def setUp(self):
        self.utm_coordinates_converter = Mock(spec=UTMCoordinatesConverter)
        self.conversion_strategy = DecimalDegreesCoordinateConversionStrategy(self.utm_coordinates_converter)

    def test_to_utm_should_convert_decimal_degrees_to_utm(self):
        self.utm_coordinates_converter.decimal_degrees_to_utm.side_effect = self._fake_conversion

        easting, northing = self.conversion_strategy.to_utm(self.LATITUDE, self.LONGITUDE)

        self.assertEqual(easting, self.EASTING)
        self.assertEqual(northing, self.NORTHING)

    def test_to_decimal_degrees_should_return_same_coordinates(self):
        latitude, longitude = self.conversion_strategy.to_decimal_degrees(self.LATITUDE, self.LONGITUDE)

        self.assertEqual(latitude, self.LATITUDE)
        self.assertEqual(longitude, self.LONGITUDE)

    def _fake_conversion(self, latitude: float, longitude: float):   # TODO: use mockito for this
        if latitude == self.LATITUDE and longitude == self.LONGITUDE:
            return self.EASTING, self.NORTHING
