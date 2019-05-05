import abc

from src.rocket_packet import RocketPacket


class RocketPacketParser:
    __metaclass__ = abc.ABCMeta

    def __init__(self, version: int, packet_format: str, num_bytes: int):
        self.version = version
        self.format = packet_format
        self.num_bytes = num_bytes

    def get_number_of_bytes(self):
        return self.num_bytes

    def get_version(self) -> int:
        return self.version

    @abc.abstractmethod
    def parse(self, data: bytes) -> RocketPacket:
        pass

    @abc.abstractmethod
    def get_field_names(self):
        pass

    @abc.abstractmethod
    def to_list(self, packet: RocketPacket) -> list:
        pass

    @abc.abstractmethod
    def from_list(self, data: list) -> RocketPacket:
        pass
