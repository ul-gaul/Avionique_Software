import abc
from typing import List, Tuple


class DataPersister:
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        pass

    @abc.abstractmethod
    def save(self, filename: str, rocket_packet_version: int, field_names: List[str],
             all_rocket_packets_fields: List[List]):
        pass

    @abc.abstractmethod
    def load(self, filename: str) -> Tuple[int, List[List]]:
        pass
