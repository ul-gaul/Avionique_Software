import csv
import errno
import os
import unittest

from src.persistence.csv_data_persister import CsvDataPersister
from src.rocket_packet.rocket_packet import RocketPacket


class CsvDataPersisterTest(unittest.TestCase):
    TEST_FILENAME = "tests/resources/test.csv"
    TEMPORARY_FILENAME = "tmp.csv"
    NUMBER_OF_FIELDS = len(RocketPacket.keys())
    ALL_ROCKET_PACKETS_FIELDS = []
    ROCKET_PACKET_FIELD_NAMES = []
    ROCKET_PACKET_VERSION = 2019

    def setUp(self):
        data_list0 = [i * 10 for i in range(self.NUMBER_OF_FIELDS)]
        data_list1 = [i * 10 + 1 for i in range(self.NUMBER_OF_FIELDS)]
        data_list2 = [i * 10 + 2 for i in range(self.NUMBER_OF_FIELDS)]
        self.ALL_ROCKET_PACKETS_FIELDS = [data_list0, data_list1, data_list2]
        self.ROCKET_PACKET_FIELD_NAMES = ["field" + str(i) for i in range(self.NUMBER_OF_FIELDS)]

        self.persister = CsvDataPersister()

    def test_save_should_write_packet_version_on_first_line(self):
        self.persister.save(self.TEMPORARY_FILENAME, self.ROCKET_PACKET_VERSION, self.ROCKET_PACKET_FIELD_NAMES,
                            self.ALL_ROCKET_PACKETS_FIELDS)

        version = self.read_version_from_file(self.TEMPORARY_FILENAME)
        self.assertEquals(version, str(self.ROCKET_PACKET_VERSION))

    def test_save_should_write_rocketPacket_field_names_as_header(self):
        self.persister.save(self.TEMPORARY_FILENAME, self.ROCKET_PACKET_VERSION, self.ROCKET_PACKET_FIELD_NAMES,
                            self.ALL_ROCKET_PACKETS_FIELDS)

        headers = self.read_headers_from_file(self.TEMPORARY_FILENAME)
        self.assertEqual(headers, self.ROCKET_PACKET_FIELD_NAMES)

    def test_load_should_return_rocket_packet_version_loaded_from_first_line(self):
        version, _ = self.persister.load(self.TEST_FILENAME)
        self.assertEqual(version, self.ROCKET_PACKET_VERSION)

    def test_load_should_return_rocket_packets_fields(self):
        _, rocket_packets_fields = self.persister.load(self.TEST_FILENAME)

        self.assertEqual(len(rocket_packets_fields), 3)
        self.assertEqual(len(rocket_packets_fields[0]), self.NUMBER_OF_FIELDS)

    def test_save_load(self):
        self.persister.save(self.TEMPORARY_FILENAME, self.ROCKET_PACKET_VERSION, self.ROCKET_PACKET_FIELD_NAMES,
                            self.ALL_ROCKET_PACKETS_FIELDS)

        version, loaded_packets_fields = self.persister.load(self.TEMPORARY_FILENAME)

        self.assertEqual(version, self.ROCKET_PACKET_VERSION)
        self.assertEqual(loaded_packets_fields, self.ALL_ROCKET_PACKETS_FIELDS)

    def read_version_from_file(self, filename: str):
        with open(filename, newline=self.persister.newline) as file:
            reader = csv.reader(file, delimiter=self.persister.delimiter)
            version_line = next(reader)
        return version_line[0]

    def read_headers_from_file(self, filename: str):
        with open(filename, newline=self.persister.newline) as file:
            reader = csv.reader(file, delimiter=self.persister.delimiter)
            next(reader)  # Skip packet version
            headers = next(reader)
        return headers

    def tearDown(self):
        self.ALL_ROCKET_PACKETS_FIELDS = []
        try:
            os.remove(self.TEMPORARY_FILENAME)
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise
