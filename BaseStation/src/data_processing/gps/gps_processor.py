from src.data_processing.gps.coordinate_conversion_strategy import CoordinateConversionStrategy
from src.data_processing.gps.gps_fix_validator import GpsFixValidator
from src.rocket_packet.rocket_packet import RocketPacket


class GpsProcessor:

    def __init__(self, initialisation_delay_in_seconds: float, gps_fix_validator: GpsFixValidator,
                 coordinate_conversion_strategy: CoordinateConversionStrategy):
        self._initialisation_delay = initialisation_delay_in_seconds
        self._gps_fix_validator = gps_fix_validator
        self._coordinate_conversion_strategy = coordinate_conversion_strategy
        self._easting = []
        self._northing = []
        self._initialisation_easting = []
        self._initialisation_northing = []
        self._base_camp_easting = None
        self._base_camp_northing = None
        self._last_latitude = 0.0
        self._last_longitude = 0.0
        self._first_gps_fix_timestamp = None
        self._initializing_gps = True

    def update(self, rocket_packet: RocketPacket):
        if self._gps_fix_validator.is_fixed(rocket_packet):
            if self._first_gps_fix_timestamp is None:
                self._first_gps_fix_timestamp = rocket_packet.time_stamp

            self._last_latitude, self._last_longitude = self._coordinate_conversion_strategy.to_decimal_degrees(
                rocket_packet.latitude, rocket_packet.longitude)
            easting, northing = self._coordinate_conversion_strategy.to_utm(rocket_packet.latitude,
                                                                            rocket_packet.longitude)

            elapsed_time = rocket_packet.time_stamp - self._first_gps_fix_timestamp

            if self._initializing_gps and elapsed_time >= self._initialisation_delay:
                self._base_camp_easting = self._average(self._initialisation_easting)
                self._base_camp_northing = self._average(self._initialisation_northing)
                self._initializing_gps = False

            if elapsed_time < self._initialisation_delay:
                self._initialisation_easting.append(easting)
                self._initialisation_northing.append(northing)
                self._easting.append(0)
                self._northing.append(0)
                self._initializing_gps = True
            else:
                self._easting.append(easting - self._base_camp_easting)
                self._northing.append(northing - self._base_camp_northing)
                self._initializing_gps = False

    @staticmethod
    def _average(data: list):
        return sum(data) / len(data)

    def get_last_coordinates(self):
        return self._last_latitude, self._last_longitude

    def get_projected_coordinates(self):
        return self._easting, self._northing

    def reset(self):
        self._easting = []
        self._northing = []
        self._initialisation_easting = []
        self._initialisation_northing = []
        self._base_camp_easting = None
        self._base_camp_northing = None
        self._last_latitude = 0.0
        self._last_longitude = 0.0
        self._first_gps_fix_timestamp = None
        self._initializing_gps = True
