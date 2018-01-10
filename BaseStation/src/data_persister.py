import abc
from typing import List

from src.rocket_packet import RocketPacket


class DataPersister:
    __metaclass__ = abc.ABCMeta

    def __init__(self, save_file_path: str):
        self.save_file_path = save_file_path

    @abc.abstractmethod
    def save(self, rocket_packets: List[RocketPacket]):
        pass
