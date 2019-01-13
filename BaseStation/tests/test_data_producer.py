import threading
import unittest

from src.data_producer import DataProducer
from src.rocket_packet import RocketPacket


class DataProducerTest(unittest.TestCase):

    def setUp(self):
        lock = threading.Lock()
        self.data_producer = DataProducer(lock)

    def test_get_available_rocket_packets_should_return_copy_of_packet_list(self):
        self.data_producer.add_rocket_packet(RocketPacket())

        copy = self.data_producer.get_available_rocket_packets()

        self.assertEqual(copy, self.data_producer.available_rocket_packets)
        self.assertFalse(copy is self.data_producer.available_rocket_packets)

    def test_add_rocket_packet_should_add_packet_to_list(self):
        initial_packet_number = len(self.data_producer.get_available_rocket_packets())

        self.data_producer.add_rocket_packet(RocketPacket())

        final_packet_number = len(self.data_producer.get_available_rocket_packets())
        self.assertEqual(final_packet_number, initial_packet_number + 1)
