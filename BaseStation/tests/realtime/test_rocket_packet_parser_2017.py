import struct
import unittest

from src.realtime.rocket_packet_parser_2017 import RocketPacketParser2017
from src.rocket_packet import RocketPacket


class RocketPacketParser2017Test(unittest.TestCase):
    TIME_STAMP = 4.0
    ANGULAR_SPEED_X = 1.0
    ANGULAR_SPEED_Y = 300.0
    ANGULAR_SPEED_Z = -1.0
    ACCELERATION_X = 0.5
    ACCELERATION_Y = 100.0
    ACCELERATION_Z = 0.5
    ALTITUDE = 10000.0
    LATITUDE = 32.0
    LONGITUDE = -106.0
    TEMPERATURE = 50.0
    QUATERNION_W = 2.0
    QUATERNION_X = 3.0
    QUATERNION_Y = 4.0
    QUATERNION_Z = 5.0
    ACQUISITION_BOARD_STATE_1 = 1
    ACQUISITION_BOARD_STATE_2 = 1
    ACQUISITION_BOARD_STATE_3 = 1
    POWER_SUPPLY_STATE_1 = 1
    POWER_SUPPLY_STATE_2 = 1
    PAYLOAD_BOARD_STATE_1 = 1
    VOLTAGE = 3.0
    CURRENT = 0.5

    def setUp(self):
        self.parser = RocketPacketParser2017()
        self.expected_rocket_packet = self.create_expected_packet()
        self.any_rocket_packet = self.create_expected_packet()
        self.EXPECTED_FIELD_NAMES = ["time_stamp", "angular_speed_x", "angular_speed_y", "angular_speed_z",
                                     "acceleration_x", "acceleration_y", "acceleration_z", "altitude", "latitude",
                                     "longitude", "temperature", "quaternion_w", "quaternion_x", "quaternion_y",
                                     "quaternion_z", "acquisition_board_state_1", "acquisition_board_state_2",
                                     "acquisition_board_state_3", "power_supply_state_1", "power_supply_state_2",
                                     "payload_board_state_1", "voltage", "current"]
        self.data = [self.TIME_STAMP, self.ANGULAR_SPEED_X, self.ANGULAR_SPEED_Y, self.ANGULAR_SPEED_Z,
                     self.ACCELERATION_X,
                     self.ACCELERATION_Y, self.ACCELERATION_Z, self.ALTITUDE, self.LATITUDE, self.LONGITUDE,
                     self.TEMPERATURE, self.QUATERNION_W, self.QUATERNION_X, self.QUATERNION_Y, self.QUATERNION_Z,
                     self.ACQUISITION_BOARD_STATE_1, self.ACQUISITION_BOARD_STATE_2, self.ACQUISITION_BOARD_STATE_3,
                     self.POWER_SUPPLY_STATE_1, self.POWER_SUPPLY_STATE_2, self.PAYLOAD_BOARD_STATE_1, self.VOLTAGE,
                     self.CURRENT]

    def test_parse_should_return_rocket_packet_given_valid_data_bytes(self):
        data_bytes = struct.pack(self.parser.format, *self.data)

        rocket_packet = self.parser.parse(data_bytes)

        self.assertEqual(rocket_packet, self.expected_rocket_packet)

    def test_parse_should_raise_struct_error_given_invalid_data_bytes(self):
        invalid_data_bytes = bytes([])

        self.assertRaises(struct.error, self.parser.parse, invalid_data_bytes)

    def test_get_field_names_should_return_the_names_of_all_rocket_packet_2017_fields(self):
        field_names = self.parser.get_field_names()

        self.assertEquals(field_names, self.EXPECTED_FIELD_NAMES)

    def test_to_list_should_return_list_with_all_rocket_packet_2017_fields(self):
        fields = self.parser.to_list(self.any_rocket_packet)

        self.assertEquals(fields, self.data)

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
        rocket_packet.quaternion_w = self.QUATERNION_W
        rocket_packet.quaternion_x = self.QUATERNION_X
        rocket_packet.quaternion_y = self.QUATERNION_Y
        rocket_packet.quaternion_z = self.QUATERNION_Z
        rocket_packet.acquisition_board_state_1 = self.ACQUISITION_BOARD_STATE_1
        rocket_packet.acquisition_board_state_2 = self.ACQUISITION_BOARD_STATE_2
        rocket_packet.acquisition_board_state_3 = self.ACQUISITION_BOARD_STATE_3
        rocket_packet.power_supply_state_1 = self.POWER_SUPPLY_STATE_1
        rocket_packet.power_supply_state_2 = self.POWER_SUPPLY_STATE_2
        rocket_packet.payload_board_state_1 = self.PAYLOAD_BOARD_STATE_1
        rocket_packet.voltage = self.VOLTAGE
        rocket_packet.current = self.CURRENT

        return rocket_packet
