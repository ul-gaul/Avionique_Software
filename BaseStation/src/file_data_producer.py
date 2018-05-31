import threading
import time
import queue

from src.data_producer import DataProducer
from src.data_persister import DataPersister
from src.playback_state import PlaybackState


class FileDataProducer(DataProducer):

    def __init__(self, data_persister: DataPersister, filename: str, mutex: threading.Lock,
                 speed=1.0, mode=1):
        super().__init__()
        self.started_event = threading.Event()
        self.playback_state = PlaybackState(speed, mode)
        self.data = data_persister.load(filename)
        self.playback_state_mutex = mutex

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
            if (index + 1) < len(self.data):
                wait = self.data[index + 1].time_stamp - self.data[index].time_stamp
                self.playback_state_mutex.acquire()
                wait /= self.playback_state.get_speed()
                self.playback_state_mutex.release()
                time.sleep(wait)
                self.rocket_packets.put(self.data[index])
                index += 1
            elif index < len(self.data):
                self.rocket_packets.put(self.data[index])
                index += 1
            else:
                time.sleep(1)

    def fast_forward(self):
        self.playback_state_mutex.acquire()
        if self.is_going_forward():
            self._accelerate()
        elif self.is_real_speed():
            self._set_mode_forward()
        else:
            self._decelerate()
        self.playback_state_mutex.release()

    def rewind(self):
        self.playback_state_mutex.acquire()
        # todo: need to make backward production work first
        if self.is_going_backward():
            self._accelerate()
        elif self.is_real_speed():
            self._set_mode_backward()
        else:
            self._decelerate()
        self.playback_state_mutex.release()

    def _accelerate(self):
        self.playback_state.speed_up()

    def _decelerate(self):
        self.playback_state.speed_down()

    def _set_mode_forward(self):
        self.playback_state.set_mode_forward()

    def _set_mode_backward(self):
        self.playback_state.set_mode_backward()

    def is_real_speed(self):
        return self.playback_state.is_neutral()

    def is_going_forward(self):
        return self.playback_state.is_going_forward()

    def is_going_backward(self):
        return self.playback_state.is_going_backward()

    def get_speed(self):
        return self.playback_state.get_speed()

    def get_mode(self):
        return self.playback_state.get_mode()
