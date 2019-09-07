from unittest import TestCase
from unittest.mock import Mock

from src.data_processing.gps.coordinate_conversion_strategy import CoordinateConversionStrategy
from src.data_processing.gps.gps_coordinates import GpsCoordinates
from src.data_processing.gps.gps_fix_validator import GpsFixValidator
from src.data_processing.gps.gps_processor import GpsProcessor
from src.data_processing.gps.utm_coordinates import UTMCoordinates
from src.data_processing.gps.utm_coordinates_converter import UTMCoordinatesConverter
from src.rocket_packet.rocket_packet import RocketPacket
from tests.rocket_packet.rocket_packet_builder import RocketPacketBuilder


class GpsProcessorTest(TestCase):
    INITIALIZATION_DELAY_IN_SECONDS = 2
    NO_INITIALIZATION_DELAY = 0
    NO_COORDINATES = GpsCoordinates(0, 0)
    DD_LAT = 46.77930
    DD_LONG = -71.27621
    GPS_COORDINATES = GpsCoordinates(DD_LAT, DD_LONG)
    INITIAL_COORDINATES = UTMCoordinates(1234, 2345)
    MOVEMENT_EASTING = 6
    MOVEMENT_NORTHING = 7
    MOVEMENT = UTMCoordinates(MOVEMENT_EASTING, MOVEMENT_NORTHING)
    NOISE = UTMCoordinates(0.1, 0.2)

    def setUp(self):
        self.gps_fix_validator = Mock(spec=GpsFixValidator)

        self.coordinate_conversion_strategy = Mock(spec=CoordinateConversionStrategy)
        self.coordinate_conversion_strategy.to_decimal_degrees.return_value = self.GPS_COORDINATES

        self.utm_coordinates_converter = Mock(spec=UTMCoordinatesConverter)

        self.gps_processor = GpsProcessor(self.INITIALIZATION_DELAY_IN_SECONDS, self.gps_fix_validator,
                                          self.coordinate_conversion_strategy, self.utm_coordinates_converter)

    def test_update_should_ignore_packet_with_no_gps_fix(self):
        rocket_packet = RocketPacket()
        rocket_packet.latitude = 46
        rocket_packet.longitude = -71
        self.gps_fix_validator.is_fixed.return_value = False  # TODO: validate parameter

        self.gps_processor.update(rocket_packet)

        self.assertEqual(self.gps_processor.get_last_coordinates(), self.NO_COORDINATES)

    def test_update_should_update_last_coordinates_given_gps_fix(self):
        rocket_packet = RocketPacket()
        rocket_packet.time_stamp = 0.0
        self.gps_fix_validator.is_fixed.return_value = True
        self.utm_coordinates_converter.decimal_degrees_to_utm.return_value = self.INITIAL_COORDINATES

        self.gps_processor.update(rocket_packet)

        self.assertEqual(self.gps_processor.get_last_coordinates(), self.GPS_COORDINATES)

    def test_update_should_process_positions_in_reference_to_base_camp_after_initialization(self):
        rocket_packets = self.create_rocket_packet_list_of_size(4)
        self.gps_fix_validator.is_fixed.return_value = True
        self.utm_coordinates_converter.decimal_degrees_to_utm.side_effect = [self.INITIAL_COORDINATES,
                                                                             self.INITIAL_COORDINATES + self.NOISE,
                                                                             self.INITIAL_COORDINATES - self.NOISE,
                                                                             self.INITIAL_COORDINATES + self.MOVEMENT]

        for rocket_packet in rocket_packets:
            self.gps_processor.update(rocket_packet)

        self.assertEqual(self.gps_processor.get_projected_coordinates(), ([0.0, 0.0, 0.0, self.MOVEMENT_EASTING],
                                                                          [0.0, 0.0, 0.0, self.MOVEMENT_NORTHING]))

    def test_update_should_process_positions_in_reference_to_base_camp_after_initialization_given_no_delay(self):
        self.gps_processor = GpsProcessor(self.NO_INITIALIZATION_DELAY, self.gps_fix_validator,
                                          self.coordinate_conversion_strategy, self.utm_coordinates_converter)
        rocket_packets = self.create_rocket_packet_list_of_size(2)
        self.gps_fix_validator.is_fixed.return_value = True
        self.utm_coordinates_converter.decimal_degrees_to_utm.side_effect = [self.INITIAL_COORDINATES,
                                                                             self.INITIAL_COORDINATES + self.MOVEMENT]

        for rocket_packet in rocket_packets:
            self.gps_processor.update(rocket_packet)

        self.assertEqual(self.gps_processor.get_projected_coordinates(), ([0.0, self.MOVEMENT_EASTING],
                                                                          [0.0, self.MOVEMENT_NORTHING]))

    def create_rocket_packet_list_of_size(self, size: int):
        return [self.create_rocket_packet(i) for i in range(size)]

    @staticmethod
    def create_rocket_packet(time_stamp: float):
        return RocketPacketBuilder().with_timestamp(time_stamp).build()
