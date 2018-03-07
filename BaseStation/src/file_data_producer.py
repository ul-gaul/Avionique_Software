import threading
import time
import queue

from src.data_producer import DataProducer
from src.data_persister import DataPersister


class FileDataProducer(DataProducer):

    def __init__(self, data_persister: DataPersister, filename: str):
        super().__init__()
        self.data = data_persister.load(filename)

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
