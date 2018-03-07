import csv
from typing import List

from src.data_persister import DataPersister
from src.domain_error import DomainError
from src.rocket_packet import RocketPacket


class CsvDataPersister(DataPersister):

    def __init__(self):
        super().__init__()
        self.newline = ''
        self.delimiter = ','
        self.quoting = csv.QUOTE_NONNUMERIC
        self.headers = RocketPacket.keys()

    def save(self, filename: str, rocket_packets: List[RocketPacket]):
        try:
            with open(filename, "w", newline=self.newline) as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=self.headers, delimiter=self.delimiter, quoting=self.quoting)
                writer.writeheader()
                for packet in rocket_packets:
                    writer.writerow(packet.__dict__)
            print("Saved data in " + filename)  # TODO: write on the status bar of the GUI instead
        except PermissionError:
            raise DomainError("Impossible d'ouvrir le fichier " + filename)

    def load(self, filename: str):
        data = []
        with open(filename, newline=self.newline) as csv_file:
            reader = csv.reader(csv_file, delimiter=self.delimiter, quoting=self.quoting)
            next(reader, None)  # Skip headers
            for row in reader:
                if len(row) >= len(self.headers):
                    data += [RocketPacket(row)]
        csv_file.close()
        return data
