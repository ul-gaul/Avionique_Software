import unittest
import csv
import os, errno
from src.rocket_packet import RocketPacket
from src.csv_file_writer import CsvFileWriter


class CsvFileWriterTest(unittest.TestCase):

    FILENAME = "tmp.csv"

    def setUp(self):
        pass

    def test_save(self):
        number_of_fields = len(RocketPacket.keys())
        data_list0 = [i*10 for i in range(number_of_fields)]
        data_list1 = [i*10 + 1 for i in range(number_of_fields)]
        data_list2 = [i*10 + 2 for i in range(number_of_fields)]
        rocket_packets = [RocketPacket(data_list0), RocketPacket(data_list1), RocketPacket(data_list2)]

        writer = CsvFileWriter(self.FILENAME, rocket_packets)
        writer.save()

        with open(self.FILENAME, newline='') as file:
            reader = csv.reader(file, delimiter=',')
            header = next(reader)
            row1 = next(reader)
            row2 = next(reader)
            row3 = next(reader)

            self.assertEqual(header, RocketPacket.keys())
            self.assertEqual(row1, [str(i*10) for i in range(number_of_fields)])
            self.assertEqual(row2, [str(i*10 + 1) for i in range(number_of_fields)])
            self.assertEqual(row3, [str(i*10 + 2) for i in range(number_of_fields)])

    def tearDown(self):
        try:
            os.remove(self.FILENAME)
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise
