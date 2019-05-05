import unittest
import csv
import os
import errno
from unittest.mock import Mock

from src.realtime.rocket_packet_parser import RocketPacketParser
from src.rocket_packet import RocketPacket
from src.persistence.csv_data_persister import CsvDataPersister


class CsvDataPersisterTest(unittest.TestCase):
    FILENAME = "tmp.csv"
    NUMBER_OF_FIELDS = len(RocketPacket.keys())
    ROCKET_PACKETS = []
    ROCKET_PACKET_FIELD_NAMES = ["field1", "field2", "field3"]
    ROCKET_PACKET_VERSION = 2019

    def setUp(self):
        data_list0 = [i * 10 for i in range(self.NUMBER_OF_FIELDS)]
        data_list1 = [i * 10 + 1 for i in range(self.NUMBER_OF_FIELDS)]
        data_list2 = [i * 10 + 2 for i in range(self.NUMBER_OF_FIELDS)]
        self.ROCKET_PACKETS = [RocketPacket(data_list0), RocketPacket(data_list1), RocketPacket(data_list2)]

        self.rocket_packet_parser = Mock(spec=RocketPacketParser)
        self.rocket_packet_parser.get_version.return_value = self.ROCKET_PACKET_VERSION
        self.rocket_packet_parser.get_field_names.return_value = self.ROCKET_PACKET_FIELD_NAMES
        self.rocket_packet_parser.to_list.side_effect = [data_list0, data_list1, data_list2]
        self.rocket_packet_parser.from_list.side_effect = self.ROCKET_PACKETS

    def test_save_should_write_rocketPacket_field_names_as_header(self):
        persister = CsvDataPersister()

        persister.save(self.FILENAME, self.ROCKET_PACKETS, self.rocket_packet_parser)

        with open(self.FILENAME, newline=persister.newline) as file:
            reader = csv.reader(file, delimiter=persister.delimiter)
            next(reader)    # Skip packet version
            header = next(reader)
        self.assertEqual(header, self.ROCKET_PACKET_FIELD_NAMES)

    def test_save_should_write_packet_version_on_first_line(self):
        persister = CsvDataPersister()

        persister.save(self.FILENAME, self.ROCKET_PACKETS, self.rocket_packet_parser)

        with open(self.FILENAME, newline=persister.newline) as file:
            reader = csv.reader(file, delimiter=persister.delimiter)
            format_line = next(reader)
        self.assertEquals(format_line[0], str(self.ROCKET_PACKET_VERSION))

    def test_save_load(self):
        persister = CsvDataPersister()

        persister.save(self.FILENAME, self.ROCKET_PACKETS, self.rocket_packet_parser)

        loaded_packets = persister.load(self.FILENAME, self.rocket_packet_parser)
        self.assertEqual(loaded_packets, self.ROCKET_PACKETS)

    def tearDown(self):
        self.ROCKET_PACKETS = []
        try:
            os.remove(self.FILENAME)
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise
