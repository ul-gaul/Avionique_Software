from src.rocket_packet import RocketPacket


class Consumer:

    def __init__(self, producer):
        self.producer = producer
        self.data = {}
        self.has_new_data = False
        self.create_keys_from_packet_format(RocketPacket())

    def create_keys_from_packet_format(self, rocket_packet):
        for key in rocket_packet.__dict__.keys():
            self.data[key] = []

    def update(self):
        rocket_packets = self.producer.get_data()
        if len(rocket_packets) > 0:
            for packet in rocket_packets:
                # TODO: extract data from packets and process it
                pass
            self.has_new_data = True

