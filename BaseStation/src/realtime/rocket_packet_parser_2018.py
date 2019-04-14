import struct

from src.realtime.rocket_packet_parser import RocketPacketParser
from src.rocket_packet import RocketPacket


class RocketPacketParser2018(RocketPacketParser):

    def __init__(self):
        super().__init__("<Lfffffffffffff", 56)

    def parse(self, data: bytes):
        data_list = struct.unpack(self.format, data)
        return self.from_list(data_list)

    def get_field_names(self):
        return ["time_stamp", "latitude", "longitude", "altitude", "temperature", "acceleration_x", "acceleration_y",
                "acceleration_z", "magnetometer_x", "magnetometer_y", "magnetometer_z", "angular_speed_x",
                "angular_speed_y", "angular_speed_z"]

    def to_dict(self, packet: RocketPacket) -> dict:
        return {"time_stamp": packet.time_stamp, "latitude": packet.latitude, "longitude": packet.longitude,
                "altitude": packet.altitude, "temperature": packet.temperature, "acceleration_x": packet.acceleration_x,
                "acceleration_y": packet.acceleration_y, "acceleration_z": packet.acceleration_z,
                "magnetometer_x": 0, "magnetometer_y": 0, "magnetometer_z": 0,
                "angular_speed_x": packet.angular_speed_x, "angular_speed_y": packet.angular_speed_y,
                "angular_speed_z": packet.angular_speed_z}

    def from_list(self, data: list) -> RocketPacket:
        rocket_packet = RocketPacket()

        rocket_packet.time_stamp = data[0]
        rocket_packet.latitude = data[1]
        rocket_packet.longitude = data[2]
        rocket_packet.altitude = data[3]
        rocket_packet.temperature = data[4]
        rocket_packet.acceleration_x = data[5]
        rocket_packet.acceleration_y = data[6]
        rocket_packet.acceleration_z = data[7]
        # TODO: support magnetometer
        # rocket_packet. = data[8]
        # rocket_packet. = data[9]
        # rocket_packet. = data[10]
        rocket_packet.angular_speed_x = data[11]
        rocket_packet.angular_speed_y = data[12]
        rocket_packet.angular_speed_z = data[13]

        return rocket_packet
