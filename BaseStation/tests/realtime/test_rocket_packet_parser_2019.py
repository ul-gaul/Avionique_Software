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
    UTC_TIME = 0.0
    ALTITUDE = 10000.0
    PRESSURE = 0
    TEMPERATURE = 50.0
    ACCELERATION_X_UNCOMP = 0
    ACCELERATION_Y_UNCOMP = 0
    ACCELERATION_Z_UNCOMP = 0
    ACCELERATION_X = 0.5
    ACCELERATION_Y = 100.0
    ACCELERATION_Z = 0.5
    MAGNETOMETER_X = 0
    MAGNETOMETER_Y = 0
    MAGNETOMETER_Z = 0
    ANGULAR_SPEED_X = 1
    ANGULAR_SPEED_Y = 300
    ANGULAR_SPEED_Z = 2

    def setUp(self):
        self.parser = RocketPacketParser2019()
        self.expected_rocket_packet = self.create_expected_packet()
        self.any_rocket_packet = self.create_expected_packet()
        self.EXPECTED_FIELDS = {"time_stamp": self.TIME_STAMP, "latitude": self.LATITUDE, "longitude": self.LONGITUDE,
                                "ns_indicator": self.NS_INDICATOR, "ew_indicator": self.EW_INDICATOR,
                                "utc_time": self.UTC_TIME, "altitude": self.ALTITUDE, "pressure": self.PRESSURE,
                                "temperature": self.TEMPERATURE, "acceleration_x_uncomp": self.ACCELERATION_X_UNCOMP,
                                "acceleration_y_uncomp": self.ACCELERATION_Y_UNCOMP,
                                "acceleration_z_uncomp": self.ACCELERATION_Z_UNCOMP,
                                "acceleration_x": self.ACCELERATION_X, "acceleration_y": self.ACCELERATION_Y,
                                "acceleration_z": self.ACCELERATION_Z, "magnetometer_x": self.MAGNETOMETER_X,
                                "magnetometer_y": self.MAGNETOMETER_Y, "magnetometer_z": self.MAGNETOMETER_Z,
                                "angular_speed_x": self.ANGULAR_SPEED_X, "angular_speed_y": self.ANGULAR_SPEED_Y,
                                "angular_speed_z": self.ANGULAR_SPEED_Z}
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

        self.assertEquals(set(field_names), set(self.EXPECTED_FIELDS.keys()))

    def test_to_dict_should_return_dict_with_all_rocket_packet_2019_fields(self):
        fields = self.parser.to_dict(self.any_rocket_packet)

        self.assertEquals(fields, self.EXPECTED_FIELDS)

    def test_from_list_should_return_rocket_packet_properly_assembled(self):
        rocket_packet = self.parser.from_list(self.data)

        self.assertEquals(rocket_packet, self.create_expected_packet())

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
