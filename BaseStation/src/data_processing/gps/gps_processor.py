from src.data_processing.gps.coordinate_conversion_strategy import CoordinateConversionStrategy
from src.data_processing.gps.gps_coordinates import GpsCoordinates
from src.data_processing.gps.gps_fix_validator import GpsFixValidator
from src.rocket_packet.rocket_packet import RocketPacket


class GpsProcessor:
    def __init__(self, initialization_delay_in_seconds: float, gps_fix_validator: GpsFixValidator,
                 coordinate_conversion_strategy: CoordinateConversionStrategy):
        self._initialization_delay = initialization_delay_in_seconds
        self._gps_fix_validator = gps_fix_validator
        self._coordinate_conversion_strategy = coordinate_conversion_strategy
        self._easting = []
        self._northing = []
        self._initialization_easting = []
        self._initialization_northing = []
        self._base_camp_easting = None
        self._base_camp_northing = None
        self._last_coordinates = GpsCoordinates(0.0, 0.0)
        self._first_gps_fix_timestamp = None
        self._initializing_gps = True

    def update(self, rocket_packet: RocketPacket):
        if self._gps_fix_validator.is_fixed(rocket_packet):
            self._last_coordinates = self._coordinate_conversion_strategy.to_decimal_degrees(rocket_packet.latitude,
                                                                                             rocket_packet.longitude)
            elapsed_time = self._get_elapsed_time_since_first_gps_fix(rocket_packet)
            easting, northing = self._coordinate_conversion_strategy.to_utm(rocket_packet.latitude,
                                                                            rocket_packet.longitude)
            self._process_coordinates(elapsed_time, easting, northing)

    def _get_elapsed_time_since_first_gps_fix(self, rocket_packet: RocketPacket):
        if self._first_gps_fix_timestamp is None:
            self._first_gps_fix_timestamp = rocket_packet.time_stamp
            return 0
        else:
            return rocket_packet.time_stamp - self._first_gps_fix_timestamp

    def _process_coordinates(self, elapsed_time, easting, northing):
        if elapsed_time <= self._initialization_delay:
            self._measure_base_camp_coordinates(easting, northing)
            self._initializing_gps = True
        else:
            if self._initializing_gps:
                self._complete_initialization()
            self._measure_rocket_movement(easting, northing)

    def _measure_base_camp_coordinates(self, easting: float, northing: float):
        self._initialization_easting.append(easting)
        self._initialization_northing.append(northing)
        self._easting.append(0)
        self._northing.append(0)

    def _complete_initialization(self):
        self._base_camp_easting = self._average(self._initialization_easting)
        self._base_camp_northing = self._average(self._initialization_northing)
        self._initializing_gps = False

    def _measure_rocket_movement(self, easting: float, northing: float):
        self._easting.append(easting - self._base_camp_easting)
        self._northing.append(northing - self._base_camp_northing)

    @staticmethod
    def _average(data: list):
        return sum(data) / len(data)

    def get_last_coordinates(self) -> GpsCoordinates:
        return self._last_coordinates

    def get_projected_coordinates(self):
        return self._easting, self._northing

    def reset(self):
        self._easting = []
        self._northing = []
        self._initialization_easting = []
        self._initialization_northing = []
        self._base_camp_easting = None
        self._base_camp_northing = None
        self._last_coordinates = GpsCoordinates(0.0, 0.0)
        self._first_gps_fix_timestamp = None
        self._initializing_gps = True
