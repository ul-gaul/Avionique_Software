from unittest import TestCase
from unittest.mock import Mock

from src.data_processing.gps.coordinate_conversion_strategy import CoordinateConversionStrategy
from src.data_processing.gps.gps_fix_validator import GpsFixValidator
from src.data_processing.gps.gps_processor import GpsProcessor
from src.rocket_packet.rocket_packet import RocketPacket


class GpsProcessorTest(TestCase):
    INITIALISATION_DELAY_IN_SECONDS = 2
    NO_COORDINATES = (0.0, 0.0)
    DD_LAT = 46.77930
    DD_LONG = -71.27621
    ANY_EASTING = 1234
    ANY_NORTHING = 2345

    def setUp(self):
        self.gps_fix_validator = Mock(spec=GpsFixValidator)
        self.coordinate_conversion_strategy = Mock(spec=CoordinateConversionStrategy)

        self.gps_processor = GpsProcessor(self.INITIALISATION_DELAY_IN_SECONDS, self.gps_fix_validator,
                                          self.coordinate_conversion_strategy)

    def test_update_should_ignore_packet_with_no_gps_fix(self):
        rocket_packet = RocketPacket()
        rocket_packet.latitude = 46
        rocket_packet.longitude = -71
        self.gps_fix_validator.is_fixed.return_value = False    # TODO: validate parameter

        self.gps_processor.update(rocket_packet)

        self.assertEqual(self.gps_processor.get_last_coordinates(), self.NO_COORDINATES)

    def test_update_should_update_last_coordinates_given_gps_fix(self):
        rocket_packet = RocketPacket()
        rocket_packet.time_stamp = 0.0
        self.gps_fix_validator.is_fixed.return_value = True
        self.coordinate_conversion_strategy.to_decimal_degrees.return_value = (self.DD_LAT, self.DD_LONG)
        self.coordinate_conversion_strategy.to_utm.return_value = (self.ANY_EASTING, self.ANY_NORTHING)

        self.gps_processor.update(rocket_packet)

        self.assertEqual(self.gps_processor.get_last_coordinates(), (self.DD_LAT, self.DD_LONG))

    def test_update_should_proess_positions_in_reference_to_base_camp_after_initialisation(self):   # FIXME: this name
        rocket_packets = [self.create_rocket_packet(i) for i in range(4)]
        self.gps_fix_validator.is_fixed.return_value = True
        self.coordinate_conversion_strategy.to_decimal_degrees.return_value = (self.DD_LAT, self.DD_LONG)
        self.coordinate_conversion_strategy.to_utm.side_effect = (self.ANY_EASTING, self.ANY_NORTHING)

        for rocket_packet in rocket_packets:
            self.gps_processor.update(rocket_packet)

        self.assertEqual(self.gps_processor.get_projected_coordinates(), ([], []))

    @staticmethod
    def create_rocket_packet(time_stamp: float):
        rocket_packet = RocketPacket()
        rocket_packet.time_stamp = time_stamp
        return rocket_packet