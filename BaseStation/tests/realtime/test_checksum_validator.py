import unittest
from unittest.mock import Mock

from src.message_listener import MessageListener
from src.message_type import MessageType
from src.realtime.checksum_validator import ChecksumValidator
from tests.matchers import AnyString


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

    def test_validate_should_notify_listeners_when_invalid_checksum(self):
        data_bytes = bytes([0])
        message_listener = Mock(spec=MessageListener)
        self.checksum_validator.register_message_listener(message_listener)

        self.checksum_validator.validate(data_bytes)

        message_listener.notify.assert_called_with(AnyString(), MessageType.WARNING)
