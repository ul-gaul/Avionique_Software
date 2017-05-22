import queue
import abc


class Producer:
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.rocket_packets = queue.Queue()
        self.is_running = False
        self.thread = None

    @abc.abstractmethod
    def start(self):
        """Demarre l'acquisition"""
        pass

    def stop(self):
        self.is_running = False
        self.thread.join()

    def get_data(self):
        packet_list = []
        while not self.rocket_packets.empty():
            try:
                packet_list.append(self.rocket_packets.get_nowait())
                self.rocket_packets.task_done()
            except queue.Empty:
                pass
        return packet_list

    @abc.abstractmethod
    def run(self):
        """Fonction du thread d'acquisition"""
        pass
