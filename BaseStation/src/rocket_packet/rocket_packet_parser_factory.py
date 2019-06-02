from src.rocket_packet.rocket_packet_parser_2017 import RocketPacketParser2017
from src.rocket_packet.rocket_packet_parser_2018 import RocketPacketParser2018
from src.rocket_packet.rocket_packet_parser_2019 import RocketPacketParser2019


class RocketPacketVersionException(Exception):
    """Raised when an invalid RocketPacket version is passed to the RocketPacketParserFactory"""


class RocketPacketParserFactory:

    @staticmethod
    def create(rocket_packet_version: int):
        if rocket_packet_version == 2017:
            return RocketPacketParser2017()
        elif rocket_packet_version == 2018:
            return RocketPacketParser2018()
        elif rocket_packet_version == 2019:
            return RocketPacketParser2019()
        else:
            raise RocketPacketVersionException("Invalid RocketPacket version {}".format(rocket_packet_version))
