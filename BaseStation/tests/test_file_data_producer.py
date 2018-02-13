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
