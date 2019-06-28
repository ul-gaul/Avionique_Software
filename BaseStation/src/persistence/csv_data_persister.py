import csv
from typing import List, Tuple

from src.data_persister import DataPersister
from src.domain_error import DomainError


class CsvDataPersister(DataPersister):

    def __init__(self):
        super().__init__()
        self.newline = ''
        self.delimiter = ','
        self.quoting = csv.QUOTE_NONNUMERIC

    def save(self, filename: str, rocket_packet_version: int, field_names: List[str],
             all_rocket_packets_fields: List[List]):
        try:
            with open(filename, "w", newline=self.newline) as csv_file:
                writer = csv.writer(csv_file, delimiter=self.delimiter, quoting=self.quoting)

                writer.writerow([rocket_packet_version])
                writer.writerow(field_names)

                for packet_fields in all_rocket_packets_fields:
                    writer.writerow(packet_fields)

        except PermissionError:
            raise DomainError("Impossible d'ouvrir le fichier " + filename)

    def load(self, filename: str) -> Tuple[int, List[List]]:
        all_rocket_packets_fields = []
        with open(filename, newline=self.newline) as csv_file:
            reader = csv.reader(csv_file, delimiter=self.delimiter, quoting=self.quoting)

            version = next(reader, None)[0]
            headers = next(reader, None)

            for rocket_packet_field in reader:
                if len(rocket_packet_field) == len(headers):
                    all_rocket_packets_fields.append(rocket_packet_field)
                else:
                    pass  # FIXME: throw exception or ignore line or put comment in the console ?
        csv_file.close()
        return version, all_rocket_packets_fields
