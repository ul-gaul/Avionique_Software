from unittest import TestCase

from parameterized import parameterized

from src.data_processing.gps.gps_fix_validator import (GpsFixValidatorFactory, IndicatorCharacterGpsFixValidator,
                                                       UtmZoneGpsFixValidator)


class GpsFixValidatorFactoryTest(TestCase):
    def setUp(self):
        self.factory = GpsFixValidatorFactory()

    @parameterized.expand([
        ("2017", 2017, UtmZoneGpsFixValidator),
        ("2018", 2018, UtmZoneGpsFixValidator),
        ("2019", 2019, IndicatorCharacterGpsFixValidator)
    ])
    def test_create_should_return_valid_gps_fix_validator_given_packet_version(self, _, version, validator_type):
        gps_fix_validator = self.factory.create(version)

        self.assertIsInstance(gps_fix_validator, validator_type)
