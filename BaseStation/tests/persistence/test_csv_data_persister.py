import unittest
import csv
import os
import errno

from src.rocket_packet import RocketPacket
from src.persistence.csv_data_persister import CsvDataPersister


class CsvDataPersisterTest(unittest.TestCase):
    FILENAME = "tmp.csv"
    NUMBER_OF_FIELDS = len(RocketPacket.keys())
    ROCKET_PACKET = []

    def setUp(self):
        data_list0 = [i * 10 for i in range(self.NUMBER_OF_FIELDS)]
        data_list1 = [i * 10 + 1 for i in range(self.NUMBER_OF_FIELDS)]
        data_list2 = [i * 10 + 2 for i in range(self.NUMBER_OF_FIELDS)]
        self.ROCKET_PACKET = [RocketPacket(data_list0), RocketPacket(data_list1), RocketPacket(data_list2)]

    def test_save_should_write_rocketPacket_keys_as_header(self):
        persister = CsvDataPersister()

        persister.save(self.FILENAME, self.ROCKET_PACKET)

        with open(self.FILENAME, newline=persister.newline) as file:
            reader = csv.reader(file, delimiter=persister.delimiter)
            header = next(reader)
        self.assertEqual(header, RocketPacket.keys())

    def test_export_import(self):
        persister = CsvDataPersister()

        persister.save(self.FILENAME, self.ROCKET_PACKET)

        loaded_packets = persister.load(self.FILENAME)
        self.assertEqual(loaded_packets, self.ROCKET_PACKET)

    def tearDown(self):
        self.ROCKET_PACKET = []
        try:
            os.remove(self.FILENAME)
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise
