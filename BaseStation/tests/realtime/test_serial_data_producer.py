import threading
import unittest
from unittest.mock import Mock

from src.data_persister import DataPersister
from src.realtime.checksum_validator import ChecksumValidator
from src.realtime.rocket_packet_parser_2017 import RocketPacketParser2017
from src.realtime.serial_data_producer import SerialDataProducer


class SerialDataProducerTest(unittest.TestCase):

    BYTES_IN_PACKET = 74
    SAVE_FILE_PATH = "foo/bar.csv"

    def setUp(self):
        self.lock = Mock(spec=threading.Lock)
        self.data_persister = Mock(spec=DataPersister)
        self.rocket_packet_parser = Mock(spec=RocketPacketParser2017)
        self.rocket_packet_parser.get_number_of_bytes.return_value = self.BYTES_IN_PACKET
        self.checksum_validator = Mock(spec=ChecksumValidator)

        self.serial_data_producer = SerialDataProducer(self.lock, self.data_persister, self.rocket_packet_parser,
                                                       self.checksum_validator)

    def test_save_should_call_DataPersister_with_flight_data(self):
        self.serial_data_producer.save(self.SAVE_FILE_PATH)

        self.data_persister.save.assert_called_with(self.SAVE_FILE_PATH,
                                                    self.serial_data_producer.available_rocket_packets)

    def test_no_unsaved_data_after_save(self):
        self.serial_data_producer.unsaved_data = True

        self.serial_data_producer.save(self.SAVE_FILE_PATH)

        self.assertFalse(self.serial_data_producer.has_unsaved_data())
