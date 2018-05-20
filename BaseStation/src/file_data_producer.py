import threading
import time
import queue

from src.data_producer import DataProducer
from src.data_persister import DataPersister
from src.time_travel import TimeTravel


class FileDataProducer(DataProducer):

    def __init__(self, data_persister: DataPersister, filename: str, mutex: threading.Lock):
        super().__init__()
        self.started_event = threading.Event()
        self.time_travel = TimeTravel()
        self.data = data_persister.load(filename)
        self.time_travel_mutex = mutex

        for packet in self.data:
            self.rocket_packets.put(packet)

    def start(self):
        self.rocket_packets = queue.Queue()
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
            self.time_travel_mutex.acquire()
            if (index + 1) < len(self.data):
                wait = self.data[index + 1].time_stamp - self.data[index].time_stamp
                time.sleep(wait / self.time_travel.get_speed())
                self.rocket_packets.put(self.data[index])
                index += 1
            elif index < len(self.data):
                self.rocket_packets.put(self.data[index])
                index += 1
            else:
                time.sleep(1)
            self.time_travel_mutex.release()

    def accelerate(self):
        self.time_travel.speed_up()

    def decelerate(self):
        self.time_travel.speed_down()

    def set_mode_forward(self):
        self.time_travel.set_mode_forward()

    def set_mode_backward(self):
        self.time_travel.set_mode_backward()

    def is_real_speed(self):
        return self.time_travel.is_neutral()

    def is_going_forward(self):
        return self.time_travel.is_going_forward()

    def is_going_backward(self):
        return self.time_travel.is_going_backward()

    def get_speed(self):
        return self.time_travel.get_speed()
