import threading
import time

from src.data_producer import DataProducer
from src.data_persister import DataPersister
from src.playback_state import PlaybackState


class FileDataProducer(DataProducer):

    END_OF_PLAYBACK_SLEEP_DELAY = 1

    def __init__(self, data_persister: DataPersister, filename: str, data_lock: threading.Lock,
                 playback_lock: threading.Lock, speed=1.0, mode=PlaybackState.Mode.MOVE_FORWARD):
        super().__init__(data_lock)
        self.index = 0
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
        self.index = 0
        while self.is_running:
            self.started_event.wait()
            self.update_replay()

    def update_replay(self):
        if self.is_going_forward():
            self._play_next_frame()
        else:
            self._play_previous_frame()

    def _play_next_frame(self):
        if self._is_at_end_of_replay():
            time.sleep(self.END_OF_PLAYBACK_SLEEP_DELAY)
        elif self._is_on_last_packet():
            self.add_rocket_packet(self.all_rocket_packets[self.index])
            self.index += 1
        else:
            self.add_rocket_packet(self.all_rocket_packets[self.index])
            self._sleep_between_packets(self.index, self.index + 1)
            self.index += 1

    def _is_at_end_of_replay(self):
        return self.index == len(self.all_rocket_packets)

    def _sleep_between_packets(self, index_1: int, index_2: int):
        sleep_time = self.all_rocket_packets[index_2].time_stamp - self.all_rocket_packets[index_1].time_stamp

        self.playback_lock.acquire()
        sleep_time /= self.playback_state.get_speed()
        self.playback_lock.release()

        time.sleep(sleep_time)

    def _is_on_last_packet(self):
        return self.index == len(self.all_rocket_packets) - 1

    def _play_previous_frame(self):
        if self.is_at_beginning_of_replay():
            time.sleep(self.END_OF_PLAYBACK_SLEEP_DELAY)
        elif self.is_on_first_packet():
            self.pop_rocket_packet()
            self.index -= 1
        else:
            self.pop_rocket_packet()
            self.index -= 1
            self._sleep_between_packets(self.index - 1, self.index)

    def is_at_beginning_of_replay(self):
        return self.index == 0

    def is_on_first_packet(self):
        return self.index == 1

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

    def pop_rocket_packet(self):
        self.lock.acquire()
        self.available_rocket_packets.pop()
        self.lock.release()

    def clear_rocket_packets(self):
        self.lock.acquire()
        self.available_rocket_packets.clear()
        self.lock.release()
