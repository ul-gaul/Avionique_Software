from typing import List, Tuple

from src.data_persister import DataPersister
from src.rocket_packet.rocket_packet import RocketPacket
from src.rocket_packet.rocket_packet_parser import RocketPacketParser
from src.rocket_packet.rocket_packet_parser_factory import RocketPacketParserFactory


class RocketPacketRepository:

    def __init__(self, data_persister: DataPersister, rocket_packet_parser_factory: RocketPacketParserFactory):
        self.data_persister = data_persister
        self.rocket_packet_parser_factory = rocket_packet_parser_factory

    def save(self, filename: str, rocket_packets: List[RocketPacket], rocket_packet_parser: RocketPacketParser):
        all_rocket_packets_fields = [rocket_packet_parser.to_list(rocket_packet) for rocket_packet in rocket_packets]

        self.data_persister.save(filename, rocket_packet_parser.get_version(), rocket_packet_parser.get_field_names(),
                                 all_rocket_packets_fields)

    def load(self, filename: str) -> Tuple[int, List[RocketPacket]]:
        rocket_packet_version, all_rocket_packet_fields = self.data_persister.load(filename)

        rocket_packet_parser = self.rocket_packet_parser_factory.create(rocket_packet_version)

        rocket_packets = []
        for rocket_packet_fields in all_rocket_packet_fields:
            rocket_packets.append(rocket_packet_parser.from_list(rocket_packet_fields))

        return rocket_packet_version, rocket_packets
