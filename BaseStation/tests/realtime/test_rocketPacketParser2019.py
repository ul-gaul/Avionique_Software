import struct
import unittest

from src.realtime.rocket_packet_parser_2019 import RocketPacketParser2019
from src.rocket_packet import RocketPacket


class RocketPacketParser2019Test(unittest.TestCase):
    TIME_STAMP = 4.0
    LATITUDE = 32.0
    LONGITUDE = -1076.0
    NS_INDICATOR = b'N'
    EW_INDICATOR = b'W'
    UTC_TIME = 210837.1
    ALTITUDE = 10000.0
    PRESSURE = 1013
    TEMPERATURE = 50.0
    ACCELERATION_X_UNCOMP = 6
    ACCELERATION_Y_UNCOMP = 101
    ACCELERATION_Z_UNCOMP = 6
    ACCELERATION_X = 0.5
    ACCELERATION_Y = 100.0
    ACCELERATION_Z = 0.5
    MAGNETOMETER_X = 1234
    MAGNETOMETER_Y = 2345
    MAGNETOMETER_Z = 3456
    ANGULAR_SPEED_X = 1
    ANGULAR_SPEED_Y = 300
    ANGULAR_SPEED_Z = 2

    def setUp(self):
        self.parser = RocketPacketParser2019()
        self.expected_rocket_packet = self.create_expected_packet()

    def test_parse_should_return_rocket_packet_given_valid_dat_bytes(self):
        data = [self.TIME_STAMP, self.LATITUDE, self.LONGITUDE, self.NS_INDICATOR, self.EW_INDICATOR, self.UTC_TIME,
                self.ALTITUDE, self.PRESSURE, self.TEMPERATURE, self.ACCELERATION_X_UNCOMP, self.ACCELERATION_Y_UNCOMP,
                self.ACCELERATION_Z_UNCOMP, self.ACCELERATION_X, self.ACCELERATION_Y, self.ACCELERATION_Z,
                self.MAGNETOMETER_X, self.MAGNETOMETER_Y, self.MAGNETOMETER_Z, self.ANGULAR_SPEED_X,
                self.ANGULAR_SPEED_Y, self.ANGULAR_SPEED_Z]
        data_bytes = struct.pack(self.parser.format, *data)

        rocket_packet = self.parser.parse(data_bytes)

        self.assertEqual(rocket_packet, self.expected_rocket_packet)

    def test_parse_should_raise_struct_error_given_invalid_data_bytes(self):
        invalid_data_bytes = bytes([])

        self.assertRaises(struct.error, self.parser.parse, invalid_data_bytes)

    def create_expected_packet(self):
        rocket_packet = RocketPacket()

        rocket_packet.time_stamp = self.TIME_STAMP
        rocket_packet.angular_speed_x = self.ANGULAR_SPEED_X
        rocket_packet.angular_speed_y = self.ANGULAR_SPEED_Y
        rocket_packet.angular_speed_z = self.ANGULAR_SPEED_Z
        rocket_packet.acceleration_x = self.ACCELERATION_X
        rocket_packet.acceleration_y = self.ACCELERATION_Y
        rocket_packet.acceleration_z = self.ACCELERATION_Z
        rocket_packet.altitude = self.ALTITUDE
        rocket_packet.latitude = self.LATITUDE
        rocket_packet.longitude = self.LONGITUDE
        rocket_packet.temperature = self.TEMPERATURE

        return rocket_packet
