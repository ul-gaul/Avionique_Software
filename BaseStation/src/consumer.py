from src.rocket_packet import RocketPacket
from src.producer import Producer


class Consumer:

    def __init__(self, producer):
        assert isinstance(producer, Producer)
        self.producer = producer
        self.data = {}
        self.has_new_data = False
        self.create_keys_from_packet_format()

    def create_keys_from_packet_format(self):
        for key in RocketPacket.keys():
            self.data[key] = []

    def update(self):
        rocket_packets = self.producer.get_data()
        if len(rocket_packets) > 0:
            for packet in rocket_packets:
                for key, value in packet.items():
                    self.data[key].append(value)
            self.has_new_data = True

    def __getitem__(self, key):
        return self.data[key]
