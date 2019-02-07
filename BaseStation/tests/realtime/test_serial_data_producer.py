import threading
import unittest
from unittest.mock import MagicMock

from src.data_persister import DataPersister
from src.realtime.rocket_packet_parser_2017 import RocketPacketParser2017
from src.realtime.serial_data_producer import SerialDataProducer


class SerialDataProducerTest(unittest.TestCase):

    SAVE_FILE_PATH = "foo/bar.csv"

    def setUp(self):
        self.lock = threading.Lock()
        self.data_persister = DataPersister()
        self.rocket_packet_parser = RocketPacketParser2017()

    def test_save_should_call_DataPersister_with_flight_data(self):
        self.data_persister.save = MagicMock()
        serial_data_producer = SerialDataProducer(self.lock, self.data_persister, self.rocket_packet_parser)

        serial_data_producer.save(self.SAVE_FILE_PATH)

        self.data_persister.save.assert_called_with(self.SAVE_FILE_PATH, serial_data_producer.available_rocket_packets)

    def test_no_unsaved_data_after_save(self):
        self.data_persister.save = MagicMock()
        serial_data_producer = SerialDataProducer(self.lock, self.data_persister, self.rocket_packet_parser)
        serial_data_producer.unsaved_data = True

        serial_data_producer.save(self.SAVE_FILE_PATH)

        self.assertFalse(serial_data_producer.has_unsaved_data())

    def test_validate_checksum_invalid(self):
        data_bytes = bytes([0])

        is_valid = SerialDataProducer.validate_checksum(data_bytes)

        self.assertFalse(is_valid)

    def test_validate_checksum_valid(self):
        data_bytes = bytes([255])

        is_valid = SerialDataProducer.validate_checksum(data_bytes)

        self.assertTrue(is_valid)

    def test_validate_checksum_invalid_overflow(self):
        data_bytes = bytes([255, 1, 1])

        is_valid = SerialDataProducer.validate_checksum(data_bytes)

        self.assertFalse(is_valid)

    def test_validate_checksum_valid_multiple_data(self):
        data_bytes = bytes([255, 1, 255])

        is_valid = SerialDataProducer.validate_checksum(data_bytes)

        self.assertTrue(is_valid)
