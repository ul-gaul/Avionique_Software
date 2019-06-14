import threading
import unittest
from unittest.mock import MagicMock, patch

from src.replay.file_data_producer import FileDataProducer
from src.replay.playback_state import PlaybackState
from src.rocket_packet.rocket_packet import RocketPacket
from src.rocket_packet.rocket_packet_repository import RocketPacketRepository


class FileDataProducerTest(unittest.TestCase):
    SAVE_FILE_PATH = "foo/bar.csv"
    TIME_STAMP_1 = 1
    TIME_STAMP_2 = 5
    TIME_STAMP_3 = 7
    NORMAL_SPEED = 1
    FAST_SPEED = 2
    DATA_LOCK = threading.RLock()
    PLAYBACK_LOCK = threading.Lock()
    ROCKET_PACKET_VERSION = 2019

    def setUp(self):
        rocket_packet_1 = RocketPacket()
        rocket_packet_1.time_stamp = self.TIME_STAMP_1
        rocket_packet_2 = RocketPacket()
        rocket_packet_2.time_stamp = self.TIME_STAMP_2
        rocket_packet_3 = RocketPacket()
        rocket_packet_3.time_stamp = self.TIME_STAMP_3
        self.data = [rocket_packet_1, rocket_packet_2, rocket_packet_3]

        def fake_load(filename):
            return (self.ROCKET_PACKET_VERSION, self.data) if filename == self.SAVE_FILE_PATH else (None, [])

        self.rocket_packet_repository = MagicMock(spec=RocketPacketRepository)
        self.rocket_packet_repository.load.side_effect = fake_load
        self.playback_state = MagicMock(spec=PlaybackState)

        self.file_data_producer = FileDataProducer(self.rocket_packet_repository, self.DATA_LOCK, self.PLAYBACK_LOCK,
                                                   self.playback_state)

    def test_get_total_packet_count_should_return_total_number_of_packets(self):
        self.file_data_producer.load(self.SAVE_FILE_PATH)

        num_packets = self.file_data_producer.get_total_packet_count()

        self.assertEqual(num_packets, len(self.data))

    def test_load_should_load_data_from_repository(self):
        self.file_data_producer.load(self.SAVE_FILE_PATH)

        self.assertEqual(self.file_data_producer.all_rocket_packets, self.data)
        self.assertEqual(self.file_data_producer.get_available_rocket_packets(), self.data)

    def test_load_should_set_index_at_last_packet(self):
        self.file_data_producer.load(self.SAVE_FILE_PATH)

        self.assertEqual(self.file_data_producer.get_current_packet_index(), len(self.data) - 1)

    def test_load_should_set_rocket_packet_version(self):
        self.file_data_producer.load(self.SAVE_FILE_PATH)

        self.assertEqual(self.file_data_producer.get_rocket_packet_version(), self.ROCKET_PACKET_VERSION)

    def test_reset_playback_state_should_reset_playback_state(self):
        self.file_data_producer.reset_playback_state()

        self.playback_state.reset.assert_called_with()

    def test_get_current_packet_index_should_return_minus1_when_no_packet(self):
        current_index = self.file_data_producer.get_current_packet_index()

        self.assertEqual(current_index, -1)

    def test_get_current_packet_index_should_return_last_packet_index_after_load(self):
        self.file_data_producer.load(self.SAVE_FILE_PATH)

        current_index = self.file_data_producer.get_current_packet_index()

        self.assertEqual(current_index, len(self.data) - 1)

    @patch('threading.Thread')
    def test_start_should_clear_all_available_packets_if_playback_mode_forward(self, _):
        self.playback_state.is_going_forward.return_value = True

        self.file_data_producer.start()

        self.assertListEqual(self.file_data_producer.get_available_rocket_packets(), [])
        self.assertEqual(self.file_data_producer.get_current_packet_index(), -1)

    @patch('threading.Thread')
    def test_start_should_not_clear_available_packets_if_playback_mode_backward(self, _):
        self.file_data_producer.load(self.SAVE_FILE_PATH)
        self.playback_state.is_going_forward.return_value = False

        self.file_data_producer.start()

        self.assertListEqual(self.file_data_producer.get_available_rocket_packets(), self.data)
        self.assertEqual(self.file_data_producer.get_current_packet_index(), len(self.data) - 1)

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
        self.file_data_producer.load(self.SAVE_FILE_PATH)
        self.playback_state.is_going_forward.return_value = True
        self.file_data_producer.index = initial_index = len(self.data) - 3
        initial_number_of_available_packets = len(self.file_data_producer.available_rocket_packets)

        self.file_data_producer.update_replay()

        self.assertEqual(len(self.file_data_producer.available_rocket_packets), initial_number_of_available_packets + 1)
        self.assertEqual(self.file_data_producer.index, initial_index + 1)

    @patch('time.sleep')
    def test_update_replay_should_sleep_when_fast_forwarding_during_replay(self, patched_time_sleep):
        self.file_data_producer.load(self.SAVE_FILE_PATH)
        self.playback_state.get_speed.return_value = self.NORMAL_SPEED
        self.playback_state.is_going_forward.return_value = True
        self.file_data_producer.index = 0

        self.file_data_producer.update_replay()

        patched_time_sleep.assert_called_with(self.TIME_STAMP_3 - self.TIME_STAMP_2)

    @patch('time.sleep')
    def test_update_replay_should_sleep_less_when_fast_forwarding_faster_during_replay(self, patched_time_sleep):
        self.file_data_producer.load(self.SAVE_FILE_PATH)
        self.playback_state.is_going_forward.return_value = True
        self.playback_state.get_speed.return_value = self.FAST_SPEED
        self.file_data_producer.index = 0

        self.file_data_producer.update_replay()

        sleep_time = (self.TIME_STAMP_3 - self.TIME_STAMP_2) / self.FAST_SPEED
        patched_time_sleep.assert_called_with(sleep_time)

    def test_update_replay_should_push_data_when_fast_forwarding_before_last_packet(self):
        self.file_data_producer.load(self.SAVE_FILE_PATH)
        self.playback_state.is_going_forward.return_value = True
        self.file_data_producer.index = initial_index = len(self.data) - 2
        initial_number_of_available_packets = len(self.file_data_producer.available_rocket_packets)

        self.file_data_producer.update_replay()

        self.assertEqual(len(self.file_data_producer.available_rocket_packets), initial_number_of_available_packets + 1)
        self.assertEqual(self.file_data_producer.index, initial_index + 1)

    @patch('time.sleep')
    def test_update_replay_should_not_sleep_when_fast_forwarding_before_last_packet(self, patched_time_sleep):
        self.file_data_producer.load(self.SAVE_FILE_PATH)
        self.playback_state.is_going_forward.return_value = True
        self.file_data_producer.index = len(self.data) - 2

        self.file_data_producer.update_replay()

        patched_time_sleep.assert_not_called()

    @patch('time.sleep')
    def test_update_replay_should_sleep_when_fast_forwarding_at_end_of_replay(self, patched_time_sleep):
        self.file_data_producer.load(self.SAVE_FILE_PATH)
        self.playback_state.is_going_forward.return_value = True
        self.file_data_producer.index = len(self.data) - 1

        self.file_data_producer.update_replay()

        patched_time_sleep.assert_called_with(self.file_data_producer.END_OF_PLAYBACK_SLEEP_DELAY)

    @patch('time.sleep')
    def test_update_replay_should_sleep_when_rewinding_at_beginning_of_replay(self, patched_time_sleep):
        self.playback_state.is_going_forward.return_value = False
        self.file_data_producer.index = 0

        self.file_data_producer.update_replay()

        patched_time_sleep.assert_called_with(self.file_data_producer.END_OF_PLAYBACK_SLEEP_DELAY)

    def test_update_replay_should_pop_data_when_rewinding_on_second_packet(self):
        self.file_data_producer.load(self.SAVE_FILE_PATH)
        self.playback_state.is_going_forward.return_value = False
        self.file_data_producer.index = 1
        initial_number_of_available_packets = len(self.file_data_producer.available_rocket_packets)

        self.file_data_producer.update_replay()

        self.assertEqual(len(self.file_data_producer.available_rocket_packets), initial_number_of_available_packets - 1)
        self.assertEqual(self.file_data_producer.index, 0)

    @patch('time.sleep')
    def test_update_replay_should_not_sleep_when_rewinding_on_second_packet(self, patched_time_sleep):
        self.file_data_producer.load(self.SAVE_FILE_PATH)
        self.playback_state.is_going_forward.return_value = False
        self.file_data_producer.index = 1

        self.file_data_producer.update_replay()

        patched_time_sleep.assert_not_called()

    @patch('time.sleep')
    def test_update_replay_should_pop_data_when_rewinding_during_replay(self, _):
        self.file_data_producer.load(self.SAVE_FILE_PATH)
        self.playback_state.is_going_forward.return_value = False
        initial_index = self.file_data_producer.index
        initial_number_of_available_packets = len(self.file_data_producer.available_rocket_packets)

        self.file_data_producer.update_replay()

        self.assertEqual(len(self.file_data_producer.available_rocket_packets), initial_number_of_available_packets - 1)
        self.assertEqual(self.file_data_producer.index, initial_index - 1)

    @patch('time.sleep')
    def test_update_replay_should_sleep_when_rewinding_during_replay(self, patched_time_sleep):
        self.file_data_producer.load(self.SAVE_FILE_PATH)
        self.playback_state.get_speed.return_value = self.NORMAL_SPEED
        self.playback_state.is_going_forward.return_value = False

        self.file_data_producer.update_replay()

        patched_time_sleep.assert_called_with(self.TIME_STAMP_2 - self.TIME_STAMP_1)

    @patch('time.sleep')
    def test_update_replay_should_sleep_less_when_rewinding_faster_during_replay(self, patched_time_sleep):
        self.file_data_producer.load(self.SAVE_FILE_PATH)
        self.playback_state.is_going_forward.return_value = False
        self.playback_state.get_speed.return_value = self.FAST_SPEED

        self.file_data_producer.update_replay()

        sleep_time = (self.TIME_STAMP_2 - self.TIME_STAMP_1) / self.FAST_SPEED
        patched_time_sleep.assert_called_with(sleep_time)

    def test_set_current_packet_index_should_push_data_when_new_index_is_bigger(self):
        self.file_data_producer.load(self.SAVE_FILE_PATH)
        self.file_data_producer.clear_rocket_packets()
        new_index = len(self.data) - 1

        self.file_data_producer.set_current_packet_index(new_index)

        self.assertEqual(self.file_data_producer.get_current_packet_index(), new_index)
        self.assertListEqual(self.file_data_producer.get_available_rocket_packets(), self.data)

    def test_set_current_packet_index_should_pop_data_when_new_index_is_smaller(self):
        self.file_data_producer.load(self.SAVE_FILE_PATH)
        new_index = 0

        self.file_data_producer.set_current_packet_index(new_index)

        self.assertEqual(self.file_data_producer.get_current_packet_index(), new_index)
        self.assertListEqual(self.file_data_producer.get_available_rocket_packets(), self.data[0:new_index + 1])

    def test_set_current_packet_index_should_do_nothing_when_new_index_is_equal(self):
        new_index = self.file_data_producer.get_current_packet_index()
        initial_data = self.file_data_producer.get_available_rocket_packets()

        self.file_data_producer.set_current_packet_index(new_index)

        self.assertEqual(self.file_data_producer.get_current_packet_index(), new_index)
        self.assertListEqual(self.file_data_producer.get_available_rocket_packets(), initial_data)

    def test_is_suspended_should_return_true_when_event_is_cleared(self):
        self.file_data_producer.suspend()

        suspended = self.file_data_producer.is_suspended()

        self.assertTrue(suspended)

    def test_is_suspended_should_return_false_when_event_is_set(self):
        self.file_data_producer.restart()

        suspended = self.file_data_producer.is_suspended()

        self.assertFalse(suspended)
