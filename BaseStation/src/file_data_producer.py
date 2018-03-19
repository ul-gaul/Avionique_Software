import threading
import time
import queue

from src.data_producer import DataProducer
from src.data_persister import DataPersister


class FileDataProducer(DataProducer):
    """ Producteur à partir d'une source fichier
    Attributs:
        started_event (threading.Event):
            set(): Drapeau `true` pour que la production soit en cours.
            clear(): Drapeau `false` pour que la production soit en pause.
            wait(): Pour bloquer une opération jusqu'à ce que le drapeau soit `true`.
    """

    def __init__(self, data_persister: DataPersister, filename: str):
        super().__init__()
        self.started_event = threading.Event()
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
            self.started_event.wait()
            print(index)
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
