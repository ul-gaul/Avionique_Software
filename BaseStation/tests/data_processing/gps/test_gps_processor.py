from unittest import TestCase
from unittest.mock import Mock

from src.data_processing.gps.coordinate_conversion_strategy import CoordinateConversionStrategy
from src.data_processing.gps.gps_coordinates import GpsCoordinates
from src.data_processing.gps.gps_fix_validator import GpsFixValidator
from src.data_processing.gps.gps_initializer import GpsInitializer
from src.data_processing.gps.gps_processor import GpsProcessor
from src.data_processing.gps.utm_coordinates import UTMCoordinates
from src.data_processing.gps.utm_coordinates_converter import UTMCoordinatesConverter
from tests.rocket_packet.rocket_packet_builder import RocketPacketBuilder


class GpsProcessorTest(TestCase):
    TIMESTAMP = 123.4
    NO_COORDINATES = GpsCoordinates(0, 0)
    DD_LAT = 46.77930
    DD_LONG = -71.27621
    GPS_COORDINATES = GpsCoordinates(DD_LAT, DD_LONG)
    INITIAL_COORDINATES = UTMCoordinates(1234, 2345)
    MOVEMENT_EASTING = 6
    MOVEMENT_NORTHING = 7
    MOVEMENT = UTMCoordinates(MOVEMENT_EASTING, MOVEMENT_NORTHING)

    def setUp(self):
        self.gps_fix_validator = Mock(spec=GpsFixValidator)
        self.coordinate_conversion_strategy = Mock(spec=CoordinateConversionStrategy)
        self.coordinate_conversion_strategy.to_decimal_degrees.return_value = self.GPS_COORDINATES
        self.utm_coordinates_converter = Mock(spec=UTMCoordinatesConverter)
        self.gps_initializer = Mock(spec=GpsInitializer)

        self.gps_processor = GpsProcessor(self.gps_fix_validator, self.coordinate_conversion_strategy,
                                          self.utm_coordinates_converter, self.gps_initializer)

    def test_update_should_ignore_packet_with_no_gps_fix(self):
        rocket_packet = RocketPacketBuilder().with_latitude(self.DD_LAT).with_longitude(self.DD_LONG).build()
        self.gps_fix_validator.is_fixed.return_value = False  # TODO: validate parameter

        self.gps_processor.update(rocket_packet)

        self.assertEqual(self.gps_processor.get_last_coordinates(), self.NO_COORDINATES)

    def test_update_should_update_last_coordinates_given_gps_fix(self):
        rocket_packet = RocketPacketBuilder().build()
        self.gps_fix_validator.is_fixed.return_value = True
        self.utm_coordinates_converter.decimal_degrees_to_utm.return_value = self.INITIAL_COORDINATES

        self.gps_processor.update(rocket_packet)

        self.assertEqual(self.gps_processor.get_last_coordinates(), self.GPS_COORDINATES)

    def test_update_should_set_coordinates_to_zero_when_initializing(self):
        rocket_packet = RocketPacketBuilder().with_timestamp(self.TIMESTAMP).build()
        self.gps_fix_validator.is_fixed.return_value = True
        self.utm_coordinates_converter.decimal_degrees_to_utm.return_value = self.INITIAL_COORDINATES

        self.gps_processor.update(rocket_packet)

        self.gps_initializer.update.assert_called_with(self.TIMESTAMP, self.INITIAL_COORDINATES)
        self.assertEqual(self.gps_processor.get_projected_coordinates(), ([0.0], [0.0]))

    def test_update_should_process_positions_in_reference_to_base_camp_after_initialization(self):
        rocket_packet = RocketPacketBuilder().build()
        self.gps_fix_validator.is_fixed.return_value = True
        self.utm_coordinates_converter.decimal_degrees_to_utm.return_value = self.INITIAL_COORDINATES + self.MOVEMENT
        self.gps_processor.notify_initialization_complete(self.INITIAL_COORDINATES)

        self.gps_processor.update(rocket_packet)

        self.assertEqual(self.gps_processor.get_projected_coordinates(), ([self.MOVEMENT_EASTING],
                                                                          [self.MOVEMENT_NORTHING]))
