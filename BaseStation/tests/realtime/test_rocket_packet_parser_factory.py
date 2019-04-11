import unittest

from src.realtime.rocket_packet_parser_2017 import RocketPacketParser2017
from src.realtime.rocket_packet_parser_2018 import RocketPacketParser2018
from src.realtime.rocket_packet_parser_2019 import RocketPacketParser2019
from src.realtime.rocket_packet_parser_factory import RocketPacketParserFactory, RocketPacketVersionException


class RocketPacketParserFactoryTest(unittest.TestCase):

    def setUp(self):
        self.invalid_rocket_packet_version = -1

    def test_create_should_return_2017_parser_given_2017(self):
        parser = RocketPacketParserFactory.create(2017)

        self.assertTrue(isinstance(parser, RocketPacketParser2017))

    def test_create_should_return_2018_parser_given_2018(self):
        parser = RocketPacketParserFactory.create(2018)

        self.assertTrue(isinstance(parser, RocketPacketParser2018))

    def test_create_should_return_2019_parser_given_2019(self):
        parser = RocketPacketParserFactory.create(2019)

        self.assertTrue(isinstance(parser, RocketPacketParser2019))

    def test_create_should_raise_exception_given_invalid_version(self):
        self.assertRaises(RocketPacketVersionException, RocketPacketParserFactory.create,
                          self.invalid_rocket_packet_version)
