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
    SPEED = 2
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

    def test_init_should_load_data_from_data_persister(self):
        file_data_producer = FileDataProducer(self.data_persister, self.SAVE_FILE_PATH, self.DATA_LOCK,
                                              self.PLAYBACK_LOCK)

        self.data_persister.load.assert_called_with(self.SAVE_FILE_PATH)
        self.assertEqual(file_data_producer.all_rocket_packets, self.data)

    def test_accelerate_should_double_speed(self):
        initial_speed = 1.0
        final_speed = initial_speed * 2
        file_data_producer = FileDataProducer(self.data_persister, self.SAVE_FILE_PATH, self.DATA_LOCK,
                                              self.PLAYBACK_LOCK, initial_speed)

        file_data_producer._accelerate()

        self.assertEqual(file_data_producer.get_speed(), final_speed)

    def test_decelerate_should_half_speed(self):
        initial_speed = 4.0
        final_speed = initial_speed / 2
        file_data_producer = FileDataProducer(self.data_persister, self.SAVE_FILE_PATH, self.DATA_LOCK,
                                              self.PLAYBACK_LOCK, initial_speed)

        file_data_producer._decelerate()

        self.assertEqual(file_data_producer.get_speed(), final_speed)

    def test_fast_forward_should_accelerate_forward(self):
        initial_speed = 1.0
        initial_mode = PlaybackState.Mode.MOVE_FORWARD
        final_speed = initial_speed * 2
        file_data_producer = FileDataProducer(self.data_persister, self.SAVE_FILE_PATH, self.DATA_LOCK,
                                              self.PLAYBACK_LOCK, initial_speed, initial_mode)

        file_data_producer.fast_forward()

        self.assertEqual(file_data_producer.get_speed(), final_speed)

    def test_fast_forward_should_decelerate_backward(self):
        initial_speed = 4.0
        initial_mode = PlaybackState.Mode.MOVE_BACKWARD
        final_speed = initial_speed / 2
        file_data_producer = FileDataProducer(self.data_persister, self.SAVE_FILE_PATH, self.DATA_LOCK,
                                              self.PLAYBACK_LOCK, initial_speed, initial_mode)

        file_data_producer.fast_forward()

        self.assertEqual(file_data_producer.get_speed(), final_speed)

    def test_fast_forward_should_set_mode_forward_when_applicable(self):
        initial_speed = 1.0
        initial_mode = PlaybackState.Mode.MOVE_BACKWARD
        final_mode = PlaybackState.Mode.MOVE_FORWARD
        file_data_producer = FileDataProducer(self.data_persister, self.SAVE_FILE_PATH, self.DATA_LOCK,
                                              self.PLAYBACK_LOCK, initial_speed, initial_mode)

        file_data_producer.fast_forward()

        self.assertEqual(file_data_producer.get_mode(), final_mode)
        self.assertEqual(file_data_producer.get_speed(), initial_speed)

    def test_fast_forward_should_not_accelerate_beyond_max_speed(self):
        initial_speed = PlaybackState.max_speed_factor
        initial_mode = PlaybackState.Mode.MOVE_FORWARD
        file_data_producer = FileDataProducer(self.data_persister, self.SAVE_FILE_PATH, self.DATA_LOCK,
                                              self.PLAYBACK_LOCK, initial_speed, initial_mode)

        file_data_producer.fast_forward()

        self.assertEqual(file_data_producer.get_mode(), PlaybackState.Mode.MOVE_FORWARD)
        self.assertEqual(file_data_producer.get_speed(), PlaybackState.max_speed_factor)

    def test_rewind_should_accelerate_backward(self):
        initial_speed = 1.0
        initial_mode = PlaybackState.Mode.MOVE_BACKWARD
        final_speed = initial_speed * 2
        file_data_producer = FileDataProducer(self.data_persister, self.SAVE_FILE_PATH, self.DATA_LOCK,
                                              self.PLAYBACK_LOCK, initial_speed, initial_mode)

        file_data_producer.rewind()

        self.assertEqual(file_data_producer.get_speed(), final_speed)

    def test_rewind_should_decelerate_forward(self):
        initial_speed = 2.0
        initial_mode = PlaybackState.Mode.MOVE_FORWARD
        final_speed = initial_speed / 2
        file_data_producer = FileDataProducer(self.data_persister, self.SAVE_FILE_PATH, self.DATA_LOCK,
                                              self.PLAYBACK_LOCK, initial_speed, initial_mode)

        file_data_producer.rewind()

        self.assertEqual(file_data_producer.get_speed(), final_speed)
        self.assertEqual(file_data_producer.get_mode(), PlaybackState.Mode.MOVE_FORWARD)

    def test_rewind_should_set_mode_backward_when_applicable(self):
        initial_speed = 1.0
        initial_mode = PlaybackState.Mode.MOVE_FORWARD
        final_mode = PlaybackState.Mode.MOVE_BACKWARD
        file_data_producer = FileDataProducer(self.data_persister, self.SAVE_FILE_PATH, self.DATA_LOCK,
                                              self.PLAYBACK_LOCK, initial_speed, initial_mode)

        file_data_producer.rewind()

        self.assertEqual(file_data_producer.get_mode(), final_mode)
        self.assertEqual(file_data_producer.get_speed(), initial_speed)

    def test_rewind_should_not_accelerate_beyond_max_speed(self):
        initial_speed = PlaybackState.max_speed_factor
        initial_mode = PlaybackState.Mode.MOVE_BACKWARD
        file_data_producer = FileDataProducer(self.data_persister, self.SAVE_FILE_PATH, self.DATA_LOCK,
                                              self.PLAYBACK_LOCK, initial_speed, initial_mode)

        file_data_producer.rewind()

        self.assertEqual(file_data_producer.get_mode(), PlaybackState.Mode.MOVE_BACKWARD)
        self.assertEqual(file_data_producer.get_speed(), PlaybackState.max_speed_factor)

    def test_clear_rocket_packets_should_remove_all_available_rocket_packets(self):
        file_data_producer = FileDataProducer(self.data_persister, self.SAVE_FILE_PATH, self.DATA_LOCK,
                                              self.PLAYBACK_LOCK)

        file_data_producer.clear_rocket_packets()

        self.assertEqual(file_data_producer.available_rocket_packets, [])

    @patch('time.sleep')
    def test_update_replay_should_push_data_when_fast_forwarding_during_replay(self, _):
        file_data_producer = FileDataProducer(self.data_persister, self.SAVE_FILE_PATH, self.DATA_LOCK,
                                              self.PLAYBACK_LOCK)
        file_data_producer.index = initial_index = len(self.data) - 2
        initial_number_of_available_packets = len(file_data_producer.available_rocket_packets)

        file_data_producer.update_replay()

        self.assertEqual(len(file_data_producer.available_rocket_packets), initial_number_of_available_packets + 1)
        self.assertEqual(file_data_producer.index, initial_index + 1)

    @patch('time.sleep')
    def test_update_replay_should_sleep_when_fast_forwarding_during_replay(self, patched_time_sleep):
        file_data_producer = FileDataProducer(self.data_persister, self.SAVE_FILE_PATH, self.DATA_LOCK,
                                              self.PLAYBACK_LOCK)
        file_data_producer.index = len(self.data) - 2

        file_data_producer.update_replay()

        patched_time_sleep.assert_called_with(self.TIME_STAMP_2 - self.TIME_STAMP_1)

    @patch('time.sleep')
    def test_update_replay_should_sleep_less_when_fast_forwarding_during_replay(self, patched_time_sleep):
        file_data_producer = FileDataProducer(self.data_persister, self.SAVE_FILE_PATH, self.DATA_LOCK,
                                              self.PLAYBACK_LOCK, speed=self.SPEED)
        file_data_producer.index = len(self.data) - 2

        file_data_producer.update_replay()

        sleep_time = (self.TIME_STAMP_2 - self.TIME_STAMP_1) / self.SPEED
        patched_time_sleep.assert_called_with(sleep_time)

    def test_update_replay_should_push_data_when_fast_forwarding_on_last_packet(self):
        file_data_producer = FileDataProducer(self.data_persister, self.SAVE_FILE_PATH, self.DATA_LOCK,
                                              self.PLAYBACK_LOCK)
        file_data_producer.index = initial_index = len(self.data) - 1
        initial_number_of_available_packets = len(file_data_producer.available_rocket_packets)

        file_data_producer.update_replay()

        self.assertEqual(len(file_data_producer.available_rocket_packets), initial_number_of_available_packets + 1)
        self.assertEqual(file_data_producer.index, initial_index + 1)

    @patch('time.sleep')
    def test_update_replay_should_not_sleep_when_fast_forwarding_on_last_packet(self, patched_time_sleep):
        file_data_producer = FileDataProducer(self.data_persister, self.SAVE_FILE_PATH, self.DATA_LOCK,
                                              self.PLAYBACK_LOCK)
        file_data_producer.index = len(self.data) - 1

        file_data_producer.update_replay()

        patched_time_sleep.assert_not_called()

    @patch('time.sleep')
    def test_update_replay_should_sleep_when_fast_forwarding_at_end_of_replay(self, patched_time_sleep):
        file_data_producer = FileDataProducer(self.data_persister, self.SAVE_FILE_PATH, self.DATA_LOCK,
                                              self.PLAYBACK_LOCK)
        file_data_producer.index = len(self.data)

        file_data_producer.update_replay()

        patched_time_sleep.assert_called_with(file_data_producer.END_OF_PLAYBACK_SLEEP_DELAY)

    @patch('time.sleep')
    def test_update_replay_should_sleep_when_rewinding_at_beginning_of_replay(self, patched_time_sleep):
        file_data_producer = FileDataProducer(self.data_persister, self.SAVE_FILE_PATH, self.DATA_LOCK,
                                              self.PLAYBACK_LOCK, mode=PlaybackState.Mode.MOVE_BACKWARD)
        file_data_producer.index = 0

        file_data_producer.update_replay()

        patched_time_sleep.assert_called_with(file_data_producer.END_OF_PLAYBACK_SLEEP_DELAY)

    def test_update_replay_should_pop_data_when_rewinding_on_first_packet(self):
        file_data_producer = FileDataProducer(self.data_persister, self.SAVE_FILE_PATH, self.DATA_LOCK,
                                              self.PLAYBACK_LOCK, mode=PlaybackState.Mode.MOVE_BACKWARD)
        file_data_producer.index = 1
        initial_number_of_available_packets = len(file_data_producer.available_rocket_packets)

        file_data_producer.update_replay()

        self.assertEqual(len(file_data_producer.available_rocket_packets), initial_number_of_available_packets - 1)
        self.assertEqual(file_data_producer.index, 0)

    @patch('time.sleep')
    def test_update_replay_should_not_sleep_when_rewinding_on_first_packet(self, patched_time_sleep):
        file_data_producer = FileDataProducer(self.data_persister, self.SAVE_FILE_PATH, self.DATA_LOCK,
                                              self.PLAYBACK_LOCK, mode=PlaybackState.Mode.MOVE_BACKWARD)
        file_data_producer.index = 1

        file_data_producer.update_replay()

        patched_time_sleep.assert_not_called()

    @patch('time.sleep')
    def test_update_replay_should_pop_data_when_rewinding_during_replay(self, _):
        file_data_producer = FileDataProducer(self.data_persister, self.SAVE_FILE_PATH, self.DATA_LOCK,
                                              self.PLAYBACK_LOCK, mode=PlaybackState.Mode.MOVE_BACKWARD)
        file_data_producer.index = initial_index = 2
        initial_number_of_available_packets = len(file_data_producer.available_rocket_packets)

        file_data_producer.update_replay()

        self.assertEqual(len(file_data_producer.available_rocket_packets), initial_number_of_available_packets - 1)
        self.assertEqual(file_data_producer.index, initial_index - 1)

    @patch('time.sleep')
    def test_update_replay_should_sleep_when_rewinding_during_replay(self, patched_time_sleep):
        file_data_producer = FileDataProducer(self.data_persister, self.SAVE_FILE_PATH, self.DATA_LOCK,
                                              self.PLAYBACK_LOCK, mode=PlaybackState.Mode.MOVE_BACKWARD)
        file_data_producer.index = 2

        file_data_producer.update_replay()

        patched_time_sleep.assert_called_with(self.TIME_STAMP_2 - self.TIME_STAMP_1)

    @patch('time.sleep')
    def test_update_replay_should_sleep_less_when_rewinding_faster_during_replay(self, patched_time_sleep):
        file_data_producer = FileDataProducer(self.data_persister, self.SAVE_FILE_PATH, self.DATA_LOCK,
                                              self.PLAYBACK_LOCK, speed=self.SPEED,
                                              mode=PlaybackState.Mode.MOVE_BACKWARD)
        file_data_producer.index = 2

        file_data_producer.update_replay()

        sleep_time = (self.TIME_STAMP_2 - self.TIME_STAMP_1) / self.SPEED
        patched_time_sleep.assert_called_with(sleep_time)
