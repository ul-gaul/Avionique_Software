import csv
from typing import List

from src.data_persister import DataPersister
from src.rocket_packet import RocketPacket


class CsvDataPersister(DataPersister):

    def __init__(self, save_file_path: str):
        super().__init__(save_file_path)

    def save(self, rocket_packets: List[RocketPacket]):
        headers = RocketPacket.keys()

        with open(self.save_file_path, "w", newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=headers, delimiter=',')
            writer.writeheader()
            for packet in rocket_packets:
                writer.writerow(packet.__dict__)

        print("Saved data in " + str(self.save_file_path))  # TODO: write on the status bar of the GUI instead
