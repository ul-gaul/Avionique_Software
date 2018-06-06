import threading
import time

from src.data_producer import DataProducer
from src.data_persister import DataPersister
from src.playback_state import PlaybackState


class FileDataProducer(DataProducer):

    def __init__(self, data_persister: DataPersister, filename: str, data_lock: threading.Lock,
                 playback_lock: threading.Lock, speed=1.0, mode=PlaybackState.Mode.MOVE_FORWARD):
        super().__init__(data_lock)
        self.started_event = threading.Event()
        self.playback_state = PlaybackState(speed, mode)
        self.playback_lock = playback_lock
        self.all_rocket_packets = data_persister.load(filename)
        self.available_rocket_packets.extend(self.all_rocket_packets)

    def start(self):
        self.clear_rocket_packets()
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
            self.update_replay()

            if (index + 1) < len(self.all_rocket_packets):
                self.add_rocket_packet(self.all_rocket_packets[index])
                wait = self.all_rocket_packets[index + 1].time_stamp - self.all_rocket_packets[index].time_stamp
                self.playback_lock.acquire()
                wait /= self.playback_state.get_speed()
                self.playback_lock.release()
                time.sleep(wait)
                index += 1
            elif index < len(self.all_rocket_packets):
                self.add_rocket_packet(self.all_rocket_packets[index])
                index += 1
            else:
                time.sleep(1)

    def update_replay(self):
        if self.is_going_forward():
            self.play_next_frame()
        else:
            self.play_previous_frame()

    def play_next_frame(self):
        # TODO
        pass

    def play_previous_frame(self):
        # TODO
        pass

    def fast_forward(self):
        self.playback_lock.acquire()
        if self.is_going_forward():
            self._accelerate()
        elif self.is_real_speed():
            self._set_mode_forward()
        else:
            self._decelerate()
        self.playback_lock.release()

    def rewind(self):
        self.playback_lock.acquire()
        if self.is_going_backward():
            self._accelerate()
        elif self.is_real_speed():
            self._set_mode_backward()
        else:
            self._decelerate()
        self.playback_lock.release()

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

    def clear_rocket_packets(self):
        self.lock.acquire()
        self.available_rocket_packets.clear()
        self.lock.release()
