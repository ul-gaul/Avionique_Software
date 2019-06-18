from unittest import TestCase

from src.data_processing.gps.gps_fix_validator import IndicatorCharacterGpsFixValidator
from src.rocket_packet.rocket_packet import RocketPacket


class IndicatorCharacterGpsFixValidatorTest(TestCase):

    def setUp(self):
        self.gps_fix_validator = IndicatorCharacterGpsFixValidator()

    def test_is_fixed_should_return_true_given_valid_indicator_character(self):
        rocket_packet = self.create_rocket_packet(b'N', b'W')

        is_fixed = self.gps_fix_validator.is_fixed(rocket_packet)

        self.assertTrue(is_fixed)

    def test_is_fixed_should_return_false_given_no_fix_indicator_character(self):
        rocket_packet = self.create_rocket_packet(b'M', b'F')

        is_fixed = self.gps_fix_validator.is_fixed(rocket_packet)

        self.assertFalse(is_fixed)

    @staticmethod
    def create_rocket_packet(ns_indicator: bytes, ew_indicator: bytes):  # TODO: extract to a builder
        rocket_packet = RocketPacket()
        rocket_packet.ns_indicator = ns_indicator
        rocket_packet.ew_indicator = ew_indicator
        return rocket_packet
