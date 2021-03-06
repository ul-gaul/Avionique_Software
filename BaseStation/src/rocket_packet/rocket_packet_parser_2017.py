import struct

from src.rocket_packet.rocket_packet import RocketPacket
from src.rocket_packet.rocket_packet_parser import RocketPacketParser


class RocketPacketParser2017(RocketPacketParser):

    def __init__(self):
        super().__init__(2017, "<fffffffffffffffBBBBBBff", 74)

    def parse(self, data: bytes):
        data_list = struct.unpack(self.format, data)
        return self.from_list(data_list)

    def get_field_names(self):
        return ["time_stamp", "angular_speed_x", "angular_speed_y", "angular_speed_z", "acceleration_x",
                "acceleration_y", "acceleration_z", "altitude", "latitude", "longitude", "temperature", "quaternion_w",
                "quaternion_x", "quaternion_y", "quaternion_z", "acquisition_board_state_1",
                "acquisition_board_state_2", "acquisition_board_state_3", "power_supply_state_1",
                "power_supply_state_2", "payload_board_state_1", "voltage", "current"]

    def to_list(self, packet: RocketPacket) -> list:
        return [packet.time_stamp, packet.angular_speed_x, packet.angular_speed_y, packet.angular_speed_z,
                packet.acceleration_x, packet.acceleration_y, packet.acceleration_z, packet.altitude, packet.latitude,
                packet.longitude, packet.temperature, packet.quaternion_w, packet.quaternion_x, packet.quaternion_y,
                packet.quaternion_z, packet.acquisition_board_state_1, packet.acquisition_board_state_2,
                packet.acquisition_board_state_3, packet.power_supply_state_1, packet.power_supply_state_2,
                packet.payload_board_state_1, packet.voltage, packet.current]

    def from_list(self, data: list) -> RocketPacket:
        rocket_packet = RocketPacket()

        rocket_packet.time_stamp = data[0]
        rocket_packet.angular_speed_x = data[1]
        rocket_packet.angular_speed_y = data[2]
        rocket_packet.angular_speed_z = data[3]
        rocket_packet.acceleration_x = data[4]
        rocket_packet.acceleration_y = data[5]
        rocket_packet.acceleration_z = data[6]
        rocket_packet.altitude = data[7]
        rocket_packet.latitude = data[8]
        rocket_packet.longitude = data[9]
        rocket_packet.temperature = data[10]
        rocket_packet.quaternion_w = data[11]
        rocket_packet.quaternion_x = data[12]
        rocket_packet.quaternion_y = data[13]
        rocket_packet.quaternion_z = data[14]
        rocket_packet.acquisition_board_state_1 = data[15]
        rocket_packet.acquisition_board_state_2 = data[16]
        rocket_packet.acquisition_board_state_3 = data[17]
        rocket_packet.power_supply_state_1 = data[18]
        rocket_packet.power_supply_state_2 = data[19]
        rocket_packet.payload_board_state_1 = data[20]
        rocket_packet.voltage = data[21]
        rocket_packet.current = data[22]

        return rocket_packet
