from unittest import TestCase
from unittest.mock import Mock

from src.data_persister import DataPersister
from src.rocket_packet.rocket_packet import RocketPacket
from src.rocket_packet.rocket_packet_parser import RocketPacketParser
from src.rocket_packet.rocket_packet_parser_factory import RocketPacketParserFactory
from src.rocket_packet.rocket_packet_repository import RocketPacketRepository


class RocketPacketRepositoryTest(TestCase):

    A_FILENAME = "rocketPackets.csv"
    A_ROCKET_PACKET_VERSION = 2018
    ROCKET_PACKET_FIELD_NAMES = ["fieldName1", "fieldName2"]
    A_ROCKET_PACKET_FIELDS_LIST = [["rocketPacket1Field1", "rocketPacket1Field2"],
                                   ["rocketPacket2Field1", "rocketPacket2Field2"]]
    A_ROCKET_PACKET = Mock(spec=RocketPacket)
    ANOTHER_ROCKET_PACKET = Mock(spec=RocketPacket)

    def setUp(self):
        self.data_persister = Mock(spec=DataPersister)
        self.rocket_packet_parser_factory = Mock(spec=RocketPacketParserFactory)
        self.rocket_packet_parser = Mock(spec=RocketPacketParser)

        self.rocket_packet_repository = RocketPacketRepository(self.data_persister, self.rocket_packet_parser_factory)

    def test_save_should_save_rocket_packets_fields_in_data_persister(self):
        self.rocket_packet_parser.get_version.return_value = self.A_ROCKET_PACKET_VERSION
        self.rocket_packet_parser.get_field_names.return_value = self.ROCKET_PACKET_FIELD_NAMES
        self.rocket_packet_parser.to_list.side_effect = self.A_ROCKET_PACKET_FIELDS_LIST

        self.rocket_packet_repository.save(self.A_FILENAME, [self.A_ROCKET_PACKET, self.ANOTHER_ROCKET_PACKET],
                                           self.rocket_packet_parser)

        self.data_persister.save.assert_called_with(self.A_FILENAME, self.A_ROCKET_PACKET_VERSION,
                                                    self.ROCKET_PACKET_FIELD_NAMES, self.A_ROCKET_PACKET_FIELDS_LIST)

    def test_load_should_return_rocket_packets_assembled_from_fields_lists(self):
        self.data_persister.load.return_value = (self.A_ROCKET_PACKET_VERSION, self.A_ROCKET_PACKET_FIELDS_LIST)
        self.rocket_packet_parser_factory.create.return_value = self.rocket_packet_parser
        self.rocket_packet_parser.from_list.side_effect = [self.A_ROCKET_PACKET, self.ANOTHER_ROCKET_PACKET]

        rocket_packets = self.rocket_packet_repository.load(self.A_FILENAME)

        self.assertEquals(rocket_packets, [self.A_ROCKET_PACKET, self.ANOTHER_ROCKET_PACKET])

    # TODO: use mockito library to configure mocks
    # fake_load_values = {A_FILENAME: (A_ROCKET_PACKET_VERSION, A_ROCKET_PACKET_FIELDS_LIST)}
    #
    # def fake_load(self, filename):
    #     return self.fake_load_values[filename]
    #
    # fake_create_values = {A_ROCKET_PACKET_VERSION: }
    #
    # def fake_create(self, version):
    #     return self.fake_create_values[version]
