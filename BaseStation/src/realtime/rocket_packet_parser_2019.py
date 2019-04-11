import struct

from src.realtime.rocket_packet_parser import RocketPacketParser
from src.rocket_packet import RocketPacket


class RocketPacketParser2019(RocketPacketParser):

    def __init__(self):
        # FIXME: this format is for the Arduino simulator. Validate types and sizes with the acquisition team.
        super().__init__("<fffccffIfHHHfffHHHHHH", 60)

    def parse(self, data: bytes):
        data_list = struct.unpack(self.format, data)
        rocket_packet = RocketPacket()

        rocket_packet.time_stamp = data_list[0]
        rocket_packet.latitude = data_list[1]
        rocket_packet.longitude = data_list[2]

        rocket_packet.altitude = data_list[6]

        rocket_packet.temperature = data_list[8]

        rocket_packet.acceleration_x = data_list[12]
        rocket_packet.acceleration_y = data_list[13]
        rocket_packet.acceleration_z = data_list[14]

        rocket_packet.angular_speed_x = data_list[18]
        rocket_packet.angular_speed_y = data_list[19]
        rocket_packet.angular_speed_z = data_list[20]

        return rocket_packet
