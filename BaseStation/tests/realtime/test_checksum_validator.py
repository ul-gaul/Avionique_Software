import unittest

from src.realtime.checksum_validator import ChecksumValidator


class ChecksumValidatorTest(unittest.TestCase):

    def setUp(self):
        self.checksum_validator = ChecksumValidator()

    def test_validate_should_be_invalid_when_sum_of_bytes_different_from_255(self):
        data_bytes = bytes([0])

        is_valid = self.checksum_validator.validate(data_bytes)

        self.assertFalse(is_valid)

    def test_validate_should_be_valid_when_sum_of_bytes_equals_255(self):
        data_bytes = bytes([255])

        is_valid = self.checksum_validator.validate(data_bytes)

        self.assertTrue(is_valid)

    def test_validate_should_be_invalid_when_overflow_and_sum_of_bytes_different_from_255(self):
        data_bytes = bytes([255, 1, 1])

        is_valid = self.checksum_validator.validate(data_bytes)

        self.assertFalse(is_valid)

    def test_validate_should_be_valid_when_overflow_and_sum_of_bytes_equals_255(self):
        data_bytes = bytes([255, 1, 255])

        is_valid = self.checksum_validator.validate(data_bytes)

        self.assertTrue(is_valid)
