import threading
import unittest
from unittest.mock import Mock

from src.consumer import Consumer
from src.data_producer import DataProducer
from src.rocket_packet import RocketPacket


class ConsumerTest(unittest.TestCase):

    def setUp(self):
        self.sampling_frequency = 1
        self.producer = DataProducer(threading.Lock())
        self.consumer = Consumer(self.producer, self.sampling_frequency)

    def test_constructor_should_create_dictionary_with_rocket_packet_keys(self):
        self.assertTrue(set(RocketPacket().keys()).issubset(set(self.consumer.data.keys())))

    def test_getitem(self):
        time_stamps = [0, 1, 2, 3, 4, 5]

        self.consumer.data["time_stamp"] = time_stamps

        self.assertEqual(self.consumer["time_stamp"], time_stamps)
        self.assertEqual(self.consumer["altitude"], [])
        self.assertRaises(KeyError, self.consumer.__getitem__, "invalid_key")

    def test_update(self):
        number_of_properties = len(RocketPacket().keys())
        dummy_data_list1 = [i for i in range(number_of_properties)]
        dummy_data_list2 = [2 * i for i in range(number_of_properties)]
        rocket_packet_list = [RocketPacket(dummy_data_list1), RocketPacket(dummy_data_list2)]
        self.producer.get_available_rocket_packets = Mock(return_value=rocket_packet_list)

        self.consumer.update()

        self.assertEqual(len(self.consumer["time_stamp"]), 2)
        for i in range(len(rocket_packet_list)):
            for key, value in rocket_packet_list[i].items():
                self.assertEqual(self.consumer[key][i], value)

    def test_update_with_no_data(self):
        self.producer.get_available_rocket_packets = Mock(return_value=[])

        self.consumer.update()

        self.assertEqual(len(self.consumer["time_stamp"]), 0)

    def test_clear_should_remove_all_data(self):
        self.producer.get_available_rocket_packets = Mock(return_value=[RocketPacket()])
        self.consumer.update()

        self.consumer.clear()

        self.assert_consumer_contains_no_data()

    def assert_consumer_contains_no_data(self):
        for data_list in self.consumer.data.values():
            self.assertEqual(len(data_list), 0)

    def test_has_data_should_return_true_when_consumer_has_data(self):
        self.producer.get_available_rocket_packets = Mock(return_value=[RocketPacket()])
        self.consumer.update()

        consumer_has_data = self.consumer.has_data()

        self.assertTrue(consumer_has_data)

    def test_has_data_should_return_false_when_consumer_has_no_data(self):
        self.producer.get_available_rocket_packets = Mock(return_value=[])
        self.consumer.update()

        consumer_has_data = self.consumer.has_data()

        self.assertFalse(consumer_has_data)

