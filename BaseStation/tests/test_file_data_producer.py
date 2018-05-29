import threading
import unittest
from unittest.mock import MagicMock

from src.data_persister import DataPersister
from src.file_data_producer import FileDataProducer
from src.rocket_packet import RocketPacket
from src.playback_state import PlaybackState


class FileDataProducerTest(unittest.TestCase):

    SAVE_FILE_PATH = "foo/bar.csv"
    DATA = [RocketPacket(), RocketPacket()]
    MUTEX = threading.Lock()

    def test_init_should_load_data_from_data_persister(self):
        data_persister = DataPersister()
        data_persister.load = MagicMock(return_value=self.DATA)

        file_data_producer = FileDataProducer(data_persister, self.SAVE_FILE_PATH, self.MUTEX)

        data_persister.load.assert_called_with(self.SAVE_FILE_PATH)
        self.assertEqual(file_data_producer.data, self.DATA)

    def test_accelerate_should_double_speed(self):
        data_persister = DataPersister()
        data_persister.load = MagicMock(return_value=self.DATA)
        initial_speed = 1.0
        final_speed = initial_speed * 2

        file_data_producer = FileDataProducer(data_persister, self.SAVE_FILE_PATH,
                                              self.MUTEX, initial_speed)
        file_data_producer._accelerate()

        self.assertEqual(file_data_producer.get_speed(), final_speed)

    def test_decelerate_should_half_speed(self):
        data_persister = DataPersister()
        data_persister.load = MagicMock(return_value=self.DATA)
        initial_speed = 4.0
        final_speed = initial_speed / 2

        file_data_producer = FileDataProducer(data_persister, self.SAVE_FILE_PATH,
                                              self.MUTEX, initial_speed)
        file_data_producer._decelerate()

        self.assertEqual(file_data_producer.get_speed(), final_speed)

    def test_fast_forward_should_accelerate_forward(self):
        data_persister = DataPersister()
        data_persister.load = MagicMock(return_value=self.DATA)
        initial_speed = 1.0
        initial_mode = PlaybackState.Mode.MOVE_FORWARD
        final_speed = initial_speed * 2

        file_data_producer = FileDataProducer(data_persister, self.SAVE_FILE_PATH,
                                              self.MUTEX, initial_speed, initial_mode)
        file_data_producer.fast_forward()

        self.assertEqual(file_data_producer.get_speed(), final_speed)

    def test_fast_forward_should_decelerate_backward(self):
        data_persister = DataPersister()
        data_persister.load = MagicMock(return_value=self.DATA)
        initial_speed = 4.0
        initial_mode = PlaybackState.Mode.MOVE_BACKWARD
        final_speed = initial_speed / 2

        file_data_producer = FileDataProducer(data_persister, self.SAVE_FILE_PATH,
                                              self.MUTEX, initial_speed, initial_mode)
        file_data_producer.fast_forward()

        self.assertEqual(file_data_producer.get_speed(), final_speed)

    def test_fast_forward_should_set_mode_forward_when_applicable(self):
        data_persister = DataPersister()
        data_persister.load = MagicMock(return_value=self.DATA)
        initial_speed = 1.0
        initial_mode = PlaybackState.Mode.MOVE_BACKWARD
        final_mode = PlaybackState.Mode.MOVE_FORWARD

        file_data_producer = FileDataProducer(data_persister, self.SAVE_FILE_PATH,
                                              self.MUTEX, initial_speed, initial_mode)
        file_data_producer.fast_forward()

        self.assertEqual(file_data_producer.get_mode(), final_mode)

    def test_rewind_should_accelerate_backward(self):
        data_persister = DataPersister()
        data_persister.load = MagicMock(return_value=self.DATA)
        initial_speed = 1.0
        initial_mode = PlaybackState.Mode.MOVE_BACKWARD
        final_speed = initial_speed * 2

        file_data_producer = FileDataProducer(data_persister, self.SAVE_FILE_PATH,
                                              self.MUTEX, initial_speed, initial_mode)
        file_data_producer.rewind()

        self.assertEqual(file_data_producer.get_speed(), final_speed)

    def test_rewind_should_decelerate_forward(self):
        data_persister = DataPersister()
        data_persister.load = MagicMock(return_value=self.DATA)
        initial_speed = 2.0
        initial_mode = PlaybackState.Mode.MOVE_FORWARD
        final_speed = initial_speed / 2

        file_data_producer = FileDataProducer(data_persister, self.SAVE_FILE_PATH,
                                              self.MUTEX, initial_speed, initial_mode)
        file_data_producer.rewind()

        self.assertEqual(file_data_producer.get_speed(), final_speed)

    def test_rewind_should_set_mode_backward_when_applicable(self):
        data_persister = DataPersister()
        data_persister.load = MagicMock(return_value=self.DATA)
        initial_speed = 1.0
        initial_mode = PlaybackState.Mode.MOVE_FORWARD
        final_mode = PlaybackState.Mode.MOVE_BACKWARD

        file_data_producer = FileDataProducer(data_persister, self.SAVE_FILE_PATH,
                                              self.MUTEX, initial_speed, initial_mode)
        file_data_producer.rewind()

        self.assertEqual(file_data_producer.get_mode(), final_mode)
