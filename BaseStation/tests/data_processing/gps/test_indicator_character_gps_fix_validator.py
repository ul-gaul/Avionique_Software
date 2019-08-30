from unittest import TestCase

from parameterized import parameterized

from src.data_processing.gps.gps_fix_validator import IndicatorCharacterGpsFixValidator
from tests.rocket_packet.rocket_packet_builder import RocketPacketBuilder


class IndicatorCharacterGpsFixValidatorTest(TestCase):
    def setUp(self):
        self.gps_fix_validator = IndicatorCharacterGpsFixValidator()

    @parameterized.expand([
        ("NE", b'N', b'E'),
        ("NW", b'N', b'W'),
        ("SE", b'S', b'E'),
        ("SW", b'S', b'W')
    ])
    def test_is_fixed_should_return_true_given_valid_indicator_character(self, _, ns_indicator, ew_indicator):
        rocket_packet = self.create_rocket_packet(ns_indicator, ew_indicator)

        is_fixed = self.gps_fix_validator.is_fixed(rocket_packet)

        self.assertTrue(is_fixed)

    def test_is_fixed_should_return_false_given_no_fix_indicator_character(self):
        rocket_packet = self.create_rocket_packet(b'M', b'F')

        is_fixed = self.gps_fix_validator.is_fixed(rocket_packet)

        self.assertFalse(is_fixed)

    @staticmethod
    def create_rocket_packet(ns_indicator: bytes, ew_indicator: bytes):
        return RocketPacketBuilder().with_ns_indicator(ns_indicator).with_ew_indicator(ew_indicator).build()
