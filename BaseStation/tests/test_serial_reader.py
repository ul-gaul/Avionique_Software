import unittest
from unittest.mock import MagicMock

from src.serial_reader import SerialReader
from src.data_persister import DataPersister


class SerialReaderTest(unittest.TestCase):

    SAVE_FILE_PATH = "foo/bar.csv"

    @unittest.skip("Can't test this without starting the thread")
    def test_stop_calls_data_persister(self):
        data_persister = DataPersister(self.SAVE_FILE_PATH)
        data_persister.save = MagicMock()
        serial_reader = SerialReader(data_persister)

        # serial_reader.stop()

        data_persister.save.assert_called_with(serial_reader.flightData)

    def test_validate_checksum_invalid(self):
        data_array = [0]

        is_valid = SerialReader.validate_checksum(data_array)

        self.assertFalse(is_valid)

    def test_validate_checksum_valid(self):
        data_array = [255]

        is_valid = SerialReader.validate_checksum(data_array)

        self.assertTrue(is_valid)

    def test_validate_checksum_invalid_overflow(self):
        data_array = [255, 1, 1]

        is_valid = SerialReader.validate_checksum(data_array)

        self.assertFalse(is_valid)

    def test_validate_checksum_valid_multiple_data(self):
        data_array = [255, 1, 255]

        is_valid = SerialReader.validate_checksum(data_array)

        self.assertTrue(is_valid)
