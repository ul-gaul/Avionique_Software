import threading
import time

from src.data_producer import DataProducer
from src.data_persister import DataPersister


class FileDataProducer(DataProducer):

    def __init__(self, lock: threading.Lock, data_persister: DataPersister, filename: str):
        super().__init__(lock)
        self.started_event = threading.Event()
        self.accel_factor = 1.0
        self.all_rocket_packets = data_persister.load(filename)
        self.available_rocket_packets.extend(self.all_rocket_packets)

    def start(self):
        self.available_rocket_packets = []
        self.thread = threading.Thread(target=self.run, args=())
        self.is_running = True
        self.thread.start()

    def restart(self):
        self.started_event.set()
        self.started_event.wait()

    def suspend(self):
        self.started_event.clear()

    def stop(self):
        self.started_event.set()
        super().stop()

    def run(self):
        index = 0
        while self.is_running:
            self.started_event.wait()
            if (index + 1) < len(self.all_rocket_packets):
                wait = self.all_rocket_packets[index + 1].time_stamp - self.all_rocket_packets[index].time_stamp
                time.sleep(wait / self.accel_factor)
                self.available_rocket_packets.append(self.all_rocket_packets[index])
                index += 1
            elif index < len(self.all_rocket_packets):
                self.available_rocket_packets.append(self.all_rocket_packets[index])
                index += 1
            else:
                time.sleep(1)
