from src.rocket_packet.rocket_packet import RocketPacket


class RocketPacketBuilder:
    def __init__(self):
        self.timestamp = 0
        self.ns_indicator = b'N'
        self.ew_indicator = b'W'

    def with_timestamp(self, timestamp):
        self.timestamp = timestamp
        return self

    def with_ns_indicator(self, ns_indicator: bytes):
        self.ns_indicator = ns_indicator
        return self

    def with_ew_indicator(self, ew_indicator: bytes):
        self.ew_indicator = ew_indicator
        return self

    def build(self) -> RocketPacket:
        rocket_packet = RocketPacket()

        rocket_packet.time_stamp = self.timestamp
        rocket_packet.ns_indicator = self.ns_indicator
        rocket_packet.ew_indicator = self.ew_indicator

        return rocket_packet
