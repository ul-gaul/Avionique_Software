import struct
import unittest

from src.rocket_packet.rocket_packet import RocketPacket
from src.rocket_packet.rocket_packet_parser_2019 import RocketPacketParser2019


class RocketPacketParser2019Test(unittest.TestCase):
    TIME_STAMP = 4.0
    LATITUDE = 32.0
    LONGITUDE = -1076.0
    NS_INDICATOR = b'N'
    EW_INDICATOR = b'W'
    UTC_TIME = 2.0
    ALTITUDE = 10000.0
    PRESSURE = 3600
    TEMPERATURE = 50.0
    ACCELERATION_X_UNCOMP = 0
    ACCELERATION_Y_UNCOMP = 0
    ACCELERATION_Z_UNCOMP = 0
    ACCELERATION_X = 0.5
    ACCELERATION_Y = 100.0
    ACCELERATION_Z = 0.5
    MAGNETOMETER_X = 10
    MAGNETOMETER_Y = 20
    MAGNETOMETER_Z = 30
    ANGULAR_SPEED_X = 1
    ANGULAR_SPEED_Y = 300
    ANGULAR_SPEED_Z = 2

    def setUp(self):
        self.parser = RocketPacketParser2019()
        self.expected_rocket_packet = self.create_expected_packet()
        self.any_rocket_packet = self.create_expected_packet()
        self.EXPECTED_FIELD_NAMES = ["time_stamp", "latitude", "longitude", "ns_indicator", "ew_indicator", "utc_time",
                                     "altitude", "pressure", "temperature", "acceleration_x_uncomp",
                                     "acceleration_y_uncomp", "acceleration_z_uncomp", "acceleration_x",
                                     "acceleration_y", "acceleration_z", "magnetometer_x", "magnetometer_y",
                                     "magnetometer_z", "angular_speed_x", "angular_speed_y", "angular_speed_z"]
        self.data = [self.TIME_STAMP, self.LATITUDE, self.LONGITUDE, self.NS_INDICATOR, self.EW_INDICATOR,
                     self.UTC_TIME,
                     self.ALTITUDE, self.PRESSURE, self.TEMPERATURE, self.ACCELERATION_X_UNCOMP,
                     self.ACCELERATION_Y_UNCOMP,
                     self.ACCELERATION_Z_UNCOMP, self.ACCELERATION_X, self.ACCELERATION_Y, self.ACCELERATION_Z,
                     self.MAGNETOMETER_X, self.MAGNETOMETER_Y, self.MAGNETOMETER_Z, self.ANGULAR_SPEED_X,
                     self.ANGULAR_SPEED_Y, self.ANGULAR_SPEED_Z]

    def test_parse_should_return_rocket_packet_given_valid_dat_bytes(self):
        data_bytes = struct.pack(self.parser.format, *self.data)

        rocket_packet = self.parser.parse(data_bytes)

        self.assertEqual(rocket_packet, self.expected_rocket_packet)

    def test_parse_should_raise_struct_error_given_invalid_data_bytes(self):
        invalid_data_bytes = bytes([])

        self.assertRaises(struct.error, self.parser.parse, invalid_data_bytes)

    def test_get_field_names_should_return_the_name_of_all_rocket_packet_2019_field(self):
        field_names = self.parser.get_field_names()

        self.assertEquals(field_names, self.EXPECTED_FIELD_NAMES)

    def test_to_list_should_return_list_with_all_rocket_packet_2019_fields(self):
        fields = self.parser.to_list(self.any_rocket_packet)

        self.assertEquals(fields, self.data)

    def test_from_list_should_return_rocket_packet_properly_assembled(self):
        rocket_packet = self.parser.from_list(self.data)

        self.assertEquals(rocket_packet, self.expected_rocket_packet)

    def create_expected_packet(self):
        rocket_packet = RocketPacket()

        rocket_packet.time_stamp = self.TIME_STAMP
        rocket_packet.longitude = self.LONGITUDE
        rocket_packet.latitude = self.LATITUDE
        rocket_packet.NSIndicator = self.NS_INDICATOR
        rocket_packet.EWIndicator = self.EW_INDICATOR
        rocket_packet.UTCtime = self.UTC_TIME
        rocket_packet.altitude = self.ALTITUDE
        rocket_packet.temperature = self.TEMPERATURE
        rocket_packet.pressure = self.PRESSURE
        rocket_packet.acceleration_x = self.ACCELERATION_X
        rocket_packet.acceleration_y = self.ACCELERATION_Y
        rocket_packet.acceleration_z = self.ACCELERATION_Z
        rocket_packet.magnetometer_x = self.MAGNETOMETER_X
        rocket_packet.magnetometer_y = self.MAGNETOMETER_Y
        rocket_packet.magnetometer_z = self.MAGNETOMETER_Z
        rocket_packet.angular_speed_x = self.ANGULAR_SPEED_X
        rocket_packet.angular_speed_y = self.ANGULAR_SPEED_Y
        rocket_packet.angular_speed_z = self.ANGULAR_SPEED_Z

        return rocket_packet
