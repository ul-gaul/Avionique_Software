import struct
import unittest

from src.rocket_packet import RocketPacket
from src.rocket_packet_parser_2018 import RocketPacketParser2018


class RocketPacketParser2018Test(unittest.TestCase):
    TIME_STAMP = 1234
    LATITUDE = 32.0
    LONGITUDE = -106.0
    ALTITUDE = 10000.0
    TEMPERATURE = 50.0
    ACCELERATION_X = 0.5
    ACCELERATION_Y = 100.0
    ACCELERATION_Z = 0.5
    MAGNET_X = 3.0
    MAGNET_Y = 4.0
    MAGNET_Z = 5.0
    GYRO_X = 6.0
    GYRO_Y = 7.0
    GYRO_Z = 8.0

    def setUp(self):
        self.parser = RocketPacketParser2018()
        self.expected_rocket_packet = self.create_expected_packet()

    def test_parse_should_return_rocket_packet_given_valid_data_bytes(self):
        data = [self.TIME_STAMP, self.LATITUDE, self.LONGITUDE, self.ALTITUDE, self.TEMPERATURE, self.ACCELERATION_X,
                self.ACCELERATION_Y, self.ACCELERATION_Z, self.MAGNET_X, self.MAGNET_Y, self.MAGNET_Z, self.GYRO_X,
                self.GYRO_Y, self.GYRO_Z]
        data_bytes = struct.pack(self.parser.format, *data)

        rocket_packet = self.parser.parse(data_bytes)

        self.assertEqual(rocket_packet, self.expected_rocket_packet)

    def test_parse_should_raise_struct_error_given_invalid_data_bytes(self):
        invalid_data_bytes = bytes([])

        self.assertRaises(struct.error, self.parser.parse, invalid_data_bytes)

    def create_expected_packet(self):
        rocket_packet = RocketPacket()

        rocket_packet.time_stamp = self.TIME_STAMP
        rocket_packet.angular_speed_x = self.GYRO_X
        rocket_packet.angular_speed_y = self.GYRO_Y
        rocket_packet.angular_speed_z = self.GYRO_Z
        rocket_packet.acceleration_x = self.ACCELERATION_X
        rocket_packet.acceleration_y = self.ACCELERATION_Y
        rocket_packet.acceleration_z = self.ACCELERATION_Z
        rocket_packet.altitude = self.ALTITUDE
        rocket_packet.latitude = self.LATITUDE
        rocket_packet.longitude = self.LONGITUDE
        rocket_packet.temperature = self.TEMPERATURE

        return rocket_packet
