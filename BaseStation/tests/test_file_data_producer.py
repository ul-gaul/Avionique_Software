import threading
import unittest
from unittest.mock import MagicMock

from src.data_persister import DataPersister
from src.file_data_producer import FileDataProducer
from src.rocket_packet import RocketPacket


class FileDataProducerTest(unittest.TestCase):

    SAVE_FILE_PATH = "foo/bar.csv"
    DATA = [RocketPacket(), RocketPacket()]

    def setUp(self):
        self.lock = threading.Lock()
        self.data_persister = DataPersister()
        self.data_persister.load = MagicMock(return_value=self.DATA)

        self.file_data_producer = FileDataProducer(self.lock, self.data_persister, self.SAVE_FILE_PATH)

    def test_init_should_load_data_from_data_persister(self):
        self.data_persister.load.assert_called_with(self.SAVE_FILE_PATH)
        self.assertEqual(self.file_data_producer.all_rocket_packets, self.DATA)

    def test_clear_rocket_packets_should_remove_all_available_rocket_packets(self):
        self.file_data_producer.clear_rocket_packets()

        self.assertEqual(self.file_data_producer.available_rocket_packets, [])
