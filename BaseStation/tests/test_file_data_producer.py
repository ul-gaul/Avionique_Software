import threading
import unittest
from unittest.mock import MagicMock, patch

from src.data_persister import DataPersister
from src.file_data_producer import FileDataProducer
from src.rocket_packet import RocketPacket
from src.playback_state import PlaybackState


class FileDataProducerTest(unittest.TestCase):
    SAVE_FILE_PATH = "foo/bar.csv"
    TIME_STAMP_1 = 1
    TIME_STAMP_2 = 5
    NORMAL_SPEED = 1
    FAST_SPEED = 2
    DATA_LOCK = threading.Lock()
    PLAYBACK_LOCK = threading.Lock()

    def setUp(self):
        rocket_packet_1 = RocketPacket()
        rocket_packet_1.time_stamp = self.TIME_STAMP_1
        rocket_packet_2 = RocketPacket()
        rocket_packet_2.time_stamp = self.TIME_STAMP_2
        self.data = [rocket_packet_1, rocket_packet_2]

        self.data_persister = DataPersister()
        self.data_persister.load = MagicMock(return_value=self.data)

        self.playback_state = PlaybackState()
        self.playback_state.fast_forward = MagicMock()
        self.playback_state.rewind = MagicMock()

        self.file_data_producer = FileDataProducer(self.data_persister, self.SAVE_FILE_PATH, self.DATA_LOCK,
                                                   self.PLAYBACK_LOCK, self.playback_state)

    def test_get_total_packet_count_should_return_total_number_of_packets(self):
        num_packets = self.file_data_producer.get_total_packet_count()

        self.assertEqual(num_packets, len(self.data))

    def test_init_should_load_data_from_data_persister(self):
        self.data_persister.load.assert_called_with(self.SAVE_FILE_PATH)
        self.assertEqual(self.file_data_producer.all_rocket_packets, self.data)

    def test_fast_forward_should_call_playback_state(self):
        self.file_data_producer.fast_forward()

        self.playback_state.fast_forward.assert_called_with()

    def test_rewind_should_call_playback_state(self):
        self.file_data_producer.rewind()

        self.playback_state.rewind.assert_called_with()

    def test_clear_rocket_packets_should_remove_all_available_rocket_packets(self):
        self.file_data_producer.clear_rocket_packets()

        self.assertEqual(self.file_data_producer.available_rocket_packets, [])

    @patch('time.sleep')
    def test_update_replay_should_push_data_when_fast_forwarding_during_replay(self, _):
        self.file_data_producer.index = initial_index = len(self.data) - 2
        initial_number_of_available_packets = len(self.file_data_producer.available_rocket_packets)

        self.file_data_producer.update_replay()

        self.assertEqual(len(self.file_data_producer.available_rocket_packets), initial_number_of_available_packets + 1)
        self.assertEqual(self.file_data_producer.index, initial_index + 1)

    @patch('time.sleep')
    def test_update_replay_should_sleep_when_fast_forwarding_during_replay(self, patched_time_sleep):
        self.file_data_producer.index = len(self.data) - 2

        self.file_data_producer.update_replay()

        patched_time_sleep.assert_called_with(self.TIME_STAMP_2 - self.TIME_STAMP_1)

    @patch('time.sleep')
    def test_update_replay_should_sleep_less_when_fast_forwarding_faster_during_replay(self, patched_time_sleep):
        self.playback_state.get_speed = MagicMock(return_value=self.FAST_SPEED)
        self.file_data_producer.index = len(self.data) - 2

        self.file_data_producer.update_replay()

        sleep_time = (self.TIME_STAMP_2 - self.TIME_STAMP_1) / self.FAST_SPEED
        patched_time_sleep.assert_called_with(sleep_time)

    def test_update_replay_should_push_data_when_fast_forwarding_on_last_packet(self):
        self.file_data_producer.index = initial_index = len(self.data) - 1
        initial_number_of_available_packets = len(self.file_data_producer.available_rocket_packets)

        self.file_data_producer.update_replay()

        self.assertEqual(len(self.file_data_producer.available_rocket_packets), initial_number_of_available_packets + 1)
        self.assertEqual(self.file_data_producer.index, initial_index + 1)

    @patch('time.sleep')
    def test_update_replay_should_not_sleep_when_fast_forwarding_on_last_packet(self, patched_time_sleep):
        self.file_data_producer.index = len(self.data) - 1

        self.file_data_producer.update_replay()

        patched_time_sleep.assert_not_called()

    @patch('time.sleep')
    def test_update_replay_should_sleep_when_fast_forwarding_at_end_of_replay(self, patched_time_sleep):
        self.file_data_producer.index = len(self.data)

        self.file_data_producer.update_replay()

        patched_time_sleep.assert_called_with(self.file_data_producer.END_OF_PLAYBACK_SLEEP_DELAY)

    @patch('time.sleep')
    def test_update_replay_should_sleep_when_rewinding_at_beginning_of_replay(self, patched_time_sleep):
        self.playback_state.is_going_forward = MagicMock(return_value=False)
        self.file_data_producer.index = 0

        self.file_data_producer.update_replay()

        patched_time_sleep.assert_called_with(self.file_data_producer.END_OF_PLAYBACK_SLEEP_DELAY)

    def test_update_replay_should_pop_data_when_rewinding_on_first_packet(self):
        self.playback_state.is_going_forward = MagicMock(return_value=False)
        self.file_data_producer.index = 1
        initial_number_of_available_packets = len(self.file_data_producer.available_rocket_packets)

        self.file_data_producer.update_replay()

        self.assertEqual(len(self.file_data_producer.available_rocket_packets), initial_number_of_available_packets - 1)
        self.assertEqual(self.file_data_producer.index, 0)

    @patch('time.sleep')
    def test_update_replay_should_not_sleep_when_rewinding_on_first_packet(self, patched_time_sleep):
        self.playback_state.is_going_forward = MagicMock(return_value=False)
        self.file_data_producer.index = 1

        self.file_data_producer.update_replay()

        patched_time_sleep.assert_not_called()

    @patch('time.sleep')
    def test_update_replay_should_pop_data_when_rewinding_during_replay(self, _):
        self.playback_state.is_going_forward = MagicMock(return_value=False)
        self.file_data_producer.index = initial_index = 2
        initial_number_of_available_packets = len(self.file_data_producer.available_rocket_packets)

        self.file_data_producer.update_replay()

        self.assertEqual(len(self.file_data_producer.available_rocket_packets), initial_number_of_available_packets - 1)
        self.assertEqual(self.file_data_producer.index, initial_index - 1)

    @patch('time.sleep')
    def test_update_replay_should_sleep_when_rewinding_during_replay(self, patched_time_sleep):
        self.playback_state.is_going_forward = MagicMock(return_value=False)
        self.file_data_producer.index = 2

        self.file_data_producer.update_replay()

        patched_time_sleep.assert_called_with(self.TIME_STAMP_2 - self.TIME_STAMP_1)

    @patch('time.sleep')
    def test_update_replay_should_sleep_less_when_rewinding_faster_during_replay(self, patched_time_sleep):
        self.playback_state.is_going_forward = MagicMock(return_value=False)
        self.playback_state.get_speed = MagicMock(return_value=self.FAST_SPEED)
        self.file_data_producer.index = 2

        self.file_data_producer.update_replay()

        sleep_time = (self.TIME_STAMP_2 - self.TIME_STAMP_1) / self.FAST_SPEED
        patched_time_sleep.assert_called_with(sleep_time)
