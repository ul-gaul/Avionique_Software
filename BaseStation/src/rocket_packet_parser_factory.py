from src.domain_error import DomainError
from src.rocket_packet_parser_2017 import RocketPacketParser2017
from src.rocket_packet_parser_2018 import RocketPacketParser2018


class RocketPacketParserFactory:

    @staticmethod
    def create(rocket_packet_version: int):
        if rocket_packet_version == 2017:
            return RocketPacketParser2017()
        elif rocket_packet_version == 2018:
            return RocketPacketParser2018()
        else:
            raise DomainError("Invalid RocketPacket version: " + str(rocket_packet_version))
