import csv
from typing import List

from src.data_persister import DataPersister
from src.domain_error import DomainError
from src.realtime.rocket_packet_parser import RocketPacketParser
from src.rocket_packet import RocketPacket


class CsvDataPersister(DataPersister):

    def __init__(self):
        super().__init__()
        self.newline = ''
        self.delimiter = ','
        self.quoting = csv.QUOTE_NONNUMERIC

    def save(self, filename: str, rocket_packets: List[RocketPacket], rocket_packet_parser: RocketPacketParser):
        try:
            with open(filename, "w", newline=self.newline) as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=rocket_packet_parser.get_field_names(),
                                        delimiter=self.delimiter, quoting=self.quoting)
                writer.writeheader()
                for packet in rocket_packets:
                    writer.writerow(rocket_packet_parser.to_dict(packet))
        except PermissionError:
            raise DomainError("Impossible d'ouvrir le fichier " + filename)

    def load(self, filename: str, rocket_packet_parser: RocketPacketParser):
        data = []
        with open(filename, newline=self.newline) as csv_file:
            reader = csv.reader(csv_file, delimiter=self.delimiter, quoting=self.quoting)
            next(reader, None)  # Skip headers
            for row in reader:
                if len(row) >= len(rocket_packet_parser.get_field_names()):
                    data.append(rocket_packet_parser.from_list(row))
        csv_file.close()
        return data
