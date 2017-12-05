import unittest

from src.serial_reader import SerialReader


class SerialReaderTest(unittest.TestCase):

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
