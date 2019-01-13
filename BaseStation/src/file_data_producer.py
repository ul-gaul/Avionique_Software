import threading
import time

from src.data_producer import DataProducer
from src.data_persister import DataPersister
from src.playback_state import PlaybackState


class FileDataProducer(DataProducer):

    END_OF_PLAYBACK_SLEEP_DELAY = 1

    def __init__(self, data_persister: DataPersister, filename: str, data_lock: threading.RLock,
                 playback_lock: threading.Lock, playback_state: PlaybackState):
        super().__init__(data_lock)
        self.started_event = threading.Event()
        self.playback_state = playback_state
        self.playback_lock = playback_lock
        self.all_rocket_packets = data_persister.load(filename)
        self.available_rocket_packets.extend(self.all_rocket_packets)
        self.index = self.get_total_packet_count() - 1

    def get_total_packet_count(self) -> int:
        return len(self.all_rocket_packets)

    def get_current_packet_index(self) -> int:
        return self.index

    def set_current_packet_index(self, new_index: int):
        self.lock.acquire()

        if new_index > self.index:
            self.available_rocket_packets.extend(self.all_rocket_packets[self.index+1:new_index+1])
            self.index = new_index
        elif new_index < self.index:
            self.available_rocket_packets = self.available_rocket_packets[0:new_index+1]
            self.index = new_index

        self.lock.release()

    def start(self):
        if self.playback_state.is_going_forward():
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
        while self.is_running:
            self.started_event.wait()
            self.update_replay()

    def update_replay(self):
        if self.playback_state.is_going_forward():
            self._play_next_frame()
        else:
            self._play_previous_frame()

    def _play_next_frame(self):
        if self._is_at_end_of_replay():
            time.sleep(self.END_OF_PLAYBACK_SLEEP_DELAY)
        elif self._is_before_last_packet():
            self.add_next_rocket_packet()
        else:
            self.add_next_rocket_packet()
            self._sleep_between_packets(self.index, self.index + 1)

    def _is_at_end_of_replay(self):
        return self.index == self.get_total_packet_count() - 1

    def _is_before_last_packet(self):
        return self.index == self.get_total_packet_count() - 2

    def _sleep_between_packets(self, index_1: int, index_2: int):
        sleep_time = self.all_rocket_packets[index_2].time_stamp - self.all_rocket_packets[index_1].time_stamp

        self.playback_lock.acquire()
        sleep_time /= self.playback_state.get_speed()
        self.playback_lock.release()

        time.sleep(sleep_time)

    def _play_previous_frame(self):
        if self._is_at_beginning_of_replay():
            time.sleep(self.END_OF_PLAYBACK_SLEEP_DELAY)
        elif self._is_on_second_packet():
            self.pop_rocket_packet()
        else:
            self.pop_rocket_packet()
            self._sleep_between_packets(self.index - 1, self.index)

    def _is_at_beginning_of_replay(self):
        return self.index == 0

    def _is_on_second_packet(self):
        return self.index == 1

    def fast_forward(self):
        self.playback_lock.acquire()
        self.playback_state.fast_forward()
        self.playback_lock.release()

    def rewind(self):
        self.playback_lock.acquire()
        self.playback_state.rewind()
        self.playback_lock.release()

    def get_speed(self):
        return self.playback_state.get_speed()

    def get_mode(self):
        return self.playback_state.get_mode()

    def add_next_rocket_packet(self):
        self.lock.acquire()
        self.index += 1
        self.add_rocket_packet(self.all_rocket_packets[self.index])
        self.lock.release()

    def pop_rocket_packet(self):
        self.lock.acquire()
        self.available_rocket_packets.pop()
        self.index -= 1
        self.lock.release()

    def clear_rocket_packets(self):
        self.lock.acquire()
        self.available_rocket_packets.clear()
        self.index = -1
        self.lock.release()
