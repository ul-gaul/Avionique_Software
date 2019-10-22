import abc

from src.rocket_packet.rocket_packet import RocketPacket


class GpsFixValidator:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def is_fixed(self, rocket_packet: RocketPacket) -> bool:
        pass


class IndicatorCharacterGpsFixValidator(GpsFixValidator):
    def is_fixed(self, rocket_packet: RocketPacket) -> bool:
        return (self.is_valid_ns_indicator(rocket_packet.ns_indicator) and
                self.is_valid_ew_indicator(rocket_packet.ew_indicator))

    @staticmethod
    def is_valid_ns_indicator(ns_indicator: bytes):
        return ns_indicator == b'N' or ns_indicator == b'S'

    @staticmethod
    def is_valid_ew_indicator(ew_indicator: bytes):
        return ew_indicator == b'E' or ew_indicator == b'W'


class UtmZoneGpsFixValidator(GpsFixValidator):
    def is_fixed(self, rocket_packet: RocketPacket) -> bool:
        return True  # Implement this to check if the coordinates are within the UTM zone limits


class GpsFixValidatorFactory:
    def create(self, rocket_packet_version: int):
        if rocket_packet_version == 2019:
            return IndicatorCharacterGpsFixValidator()
        else:
            # TODO: use a logger for this
            print("Warning: UtmZoneGpsFixValidator is not implemented and the GPS will always be considered fixed.")
            return UtmZoneGpsFixValidator()
