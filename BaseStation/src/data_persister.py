import abc
from typing import List

from src.rocket_packet import RocketPacket


class DataPersister:
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        pass

    @abc.abstractmethod
    def save(self, filename: str, rocket_packets: List[RocketPacket]):
        pass

    @abc.abstractmethod
    def load(self, filename: str):
        pass
