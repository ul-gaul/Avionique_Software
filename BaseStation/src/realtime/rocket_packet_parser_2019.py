import struct

from src.realtime.rocket_packet_parser import RocketPacketParser
from src.rocket_packet import RocketPacket


class RocketPacketParser2019(RocketPacketParser):

    def __init__(self):
        # FIXME: this format is for the Arduino simulator. Validate types and sizes with the acquisition team.
        super().__init__("<fffccffIfHHHfffHHHHHH", 60)

    def parse(self, data: bytes):
        # TODO: support all fields
        data_list = struct.unpack(self.format, data)
        return self.from_list(data_list)

    def get_field_names(self):
        return ["time_stamp", "latitude", "longitude", "ns_indicator", "ew_indicator", "utc_time", "altitude",
                "pressure", "temperature", "acceleration_x_uncomp", "acceleration_y_uncomp", "acceleration_z_uncomp",
                "acceleration_x", "acceleration_y", "acceleration_z", "magnetometer_x", "magnetometer_y",
                "magnetometer_z", "angular_speed_x", "angular_speed_y", "angular_speed_z"]

    def to_dict(self, packet: RocketPacket) -> dict:
        return {"time_stamp": packet.time_stamp, "latitude": packet.latitude, "longitude": packet.longitude,
                "ns_indicator": b'N', "ew_indicator": b'W', "utc_time": 0.0, "altitude": packet.altitude,
                "pressure": 0, "temperature": packet.temperature, "acceleration_x_uncomp": 0,
                "acceleration_y_uncomp": 0, "acceleration_z_uncomp": 0, "acceleration_x": packet.acceleration_x,
                "acceleration_y": packet.acceleration_y, "acceleration_z": packet.acceleration_z, "magnetometer_x": 0,
                "magnetometer_y": 0, "magnetometer_z": 0, "angular_speed_x": packet.angular_speed_x,
                "angular_speed_y": packet.angular_speed_y, "angular_speed_z": packet.angular_speed_z}

    def from_list(self, data: list) -> RocketPacket:
        rocket_packet = RocketPacket()

        rocket_packet.time_stamp = data[0]
        rocket_packet.latitude = data[1]
        rocket_packet.longitude = data[2]

        rocket_packet.altitude = data[6]

        rocket_packet.temperature = data[8]

        rocket_packet.acceleration_x = data[12]
        rocket_packet.acceleration_y = data[13]
        rocket_packet.acceleration_z = data[14]

        rocket_packet.angular_speed_x = data[18]
        rocket_packet.angular_speed_y = data[19]
        rocket_packet.angular_speed_z = data[20]

        return rocket_packet
