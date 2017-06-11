import csv
from src.rocket_packet import RocketPacket


class CsvFileWriter:
    """
    Note: the save method was separated from the initialization so that we can add the possibility to save one packet at
    a time in the csv file.
    """
    def __init__(self, filename, rocket_packets):
        # TODO: validate filename or path
        self.filename = filename
        self.header = RocketPacket.keys()
        self.rocket_packets = rocket_packets

    def save(self):
        if self.filename:
            print("Saved data in " + str(self.filename))  # TODO: write on the status bar of the GUI instead
            with open(self.filename, "w", newline='') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=self.header, delimiter=',')
                writer.writeheader()
                for packet in self.rocket_packets:
                    writer.writerow(packet.__dict__)
