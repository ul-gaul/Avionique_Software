import abc


class RocketPacketParser:
    __metaclass__ = abc.ABCMeta

    def __init__(self, packet_format: str, num_bytes: int):
        self.format = packet_format
        self.num_bytes = num_bytes

    def get_number_of_bytes(self):
        return self.num_bytes

    @abc.abstractmethod
    def parse(self, data: bytes):
        pass
