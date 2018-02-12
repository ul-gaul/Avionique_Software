import unittest
from unittest.mock import MagicMock

from src.serial_data_producer import SerialDataProducer
from src.data_persister import DataPersister


class SerialDataProducerTest(unittest.TestCase):

    SAVE_FILE_PATH = "foo/bar.csv"

    def test_save_should_call_DataPersister_with_flight_data(self):
        data_persister = DataPersister()
        data_persister.save = MagicMock()
        serial_data_producer = SerialDataProducer(data_persister)

        serial_data_producer.save(self.SAVE_FILE_PATH)

        data_persister.save.assert_called_with(self.SAVE_FILE_PATH, serial_data_producer.flightData)

    def test_validate_checksum_invalid(self):
        data_array = [0]

        is_valid = SerialDataProducer.validate_checksum(data_array)

        self.assertFalse(is_valid)

    def test_validate_checksum_valid(self):
        data_array = [255]

        is_valid = SerialDataProducer.validate_checksum(data_array)

        self.assertTrue(is_valid)

    def test_validate_checksum_invalid_overflow(self):
        data_array = [255, 1, 1]

        is_valid = SerialDataProducer.validate_checksum(data_array)

        self.assertFalse(is_valid)

    def test_validate_checksum_valid_multiple_data(self):
        data_array = [255, 1, 255]

        is_valid = SerialDataProducer.validate_checksum(data_array)

        self.assertTrue(is_valid)
