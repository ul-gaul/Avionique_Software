from src.data_producer import DataProducer
from src.rocket_packet import RocketPacket
import threading
import time
import csv
import queue


class FileDataProducer(DataProducer):

    def __init__(self, file):
        super().__init__()
        self.data = []

        with open(file, newline='') as csvfile:
            # TODO: standardize the csv format used by the FileDataProducer and the FileWriter
            spamreader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
            next(spamreader, None)
            for row in spamreader:
                if len(row) >= len(RocketPacket.keys()):
                    self.data += [RocketPacket(row)]

        csvfile.close()

        for packet in self.data:
            self.rocket_packets.put(packet)

    def start(self):
        self.rocket_packets = queue.Queue()
        self.thread = threading.Thread(target=self.run, args=())
        self.is_running = True
        self.thread.start()

    def run(self):
        index = 0
        while self.is_running:
            if (index + 1) < len(self.data):
                wait = self.data[index + 1].time_stamp - self.data[index].time_stamp
                time.sleep(wait)
                self.rocket_packets.put(self.data[index])
                index += 1
            elif index < len(self.data):
                self.rocket_packets.put(self.data[index])
                index += 1
            else:
                time.sleep(1)