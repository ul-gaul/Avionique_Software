import unittest
from unittest.mock import MagicMock

from src.data_persister import DataPersister
from src.file_data_producer import FileDataProducer
from src.rocket_packet import RocketPacket


class FileDataProducerTest(unittest.TestCase):

    SAVE_FILE_PATH = "foo/bar.csv"
    DATA = [RocketPacket(), RocketPacket()]

    def test_init_should_load_data_from_data_persister(self):
        data_persister = DataPersister()
        data_persister.load = MagicMock(return_value=self.DATA)

        file_data_producer = FileDataProducer(data_persister, self.SAVE_FILE_PATH)

        data_persister.load.assert_called_with(self.SAVE_FILE_PATH)
        self.assertEqual(file_data_producer.data, self.DATA)

    def test_accelerate_should_double_speed(self):
        data_persister = DataPersister()
        data_persister.load = MagicMock(return_value=self.DATA)
        file_data_producer = FileDataProducer(data_persister, self.SAVE_FILE_PATH)
        initial_speed = file_data_producer.get_speed()
        file_data_producer.accelerate()
        self.assertEqual(file_data_producer.get_speed(), initial_speed * 2)

    def test_decelerate_should_half_speed(self):
        data_persister = DataPersister()
        data_persister.load = MagicMock(return_value=self.DATA)
        file_data_producer = FileDataProducer(data_persister, self.SAVE_FILE_PATH)
        file_data_producer.accelerate()
        initial_speed = file_data_producer.get_speed()
        file_data_producer.decelerate()
        self.assertEqual(file_data_producer.get_speed(), initial_speed / 2)
