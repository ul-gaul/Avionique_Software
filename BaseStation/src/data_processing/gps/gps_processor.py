from typing import List

from src.data_processing.gps.coordinate_conversion_strategy import CoordinateConversionStrategy
from src.data_processing.gps.gps_coordinates import GpsCoordinates
from src.data_processing.gps.gps_fix_validator import GpsFixValidator
from src.data_processing.gps.utm_coordinates import UTMCoordinates
from src.data_processing.gps.utm_coordinates_converter import UTMCoordinatesConverter
from src.rocket_packet.rocket_packet import RocketPacket


class GpsProcessor:
    def __init__(self, initialization_delay_in_seconds: float, gps_fix_validator: GpsFixValidator,
                 coordinate_conversion_strategy: CoordinateConversionStrategy,
                 utm_coordinates_converter: UTMCoordinatesConverter):
        self._initialization_delay = initialization_delay_in_seconds
        self._gps_fix_validator = gps_fix_validator
        self._coordinate_conversion_strategy = coordinate_conversion_strategy
        self._utm_coordinates_converter = utm_coordinates_converter
        self._easting = []
        self._northing = []
        self._initialization_coordinates = []
        self._base_camp_coordinates = UTMCoordinates(0.0, 0.0)
        self._last_coordinates = GpsCoordinates(0.0, 0.0)
        self._first_gps_fix_timestamp = None
        self._initializing_gps = True

    def update(self, rocket_packet: RocketPacket):
        if self._gps_fix_validator.is_fixed(rocket_packet):
            self._last_coordinates = self._coordinate_conversion_strategy.to_decimal_degrees(rocket_packet.latitude,
                                                                                             rocket_packet.longitude)
            elapsed_time = self._get_elapsed_time_since_first_gps_fix(rocket_packet)
            utm_coordinates = self._utm_coordinates_converter.decimal_degrees_to_utm(self._last_coordinates)
            self._process_coordinates(elapsed_time, utm_coordinates)

    def _get_elapsed_time_since_first_gps_fix(self, rocket_packet: RocketPacket):
        if self._first_gps_fix_timestamp is None:
            self._first_gps_fix_timestamp = rocket_packet.time_stamp
            return 0
        else:
            return rocket_packet.time_stamp - self._first_gps_fix_timestamp

    def _process_coordinates(self, elapsed_time, utm_coordinates: UTMCoordinates):
        if elapsed_time <= self._initialization_delay:
            self._measure_base_camp_coordinates(utm_coordinates)
            self._initializing_gps = True
        else:
            if self._initializing_gps:
                self._complete_initialization()
            self._measure_rocket_movement(utm_coordinates)

    def _measure_base_camp_coordinates(self, utm_coordinates: UTMCoordinates):
        self._initialization_coordinates.append(utm_coordinates)
        self._easting.append(0)
        self._northing.append(0)

    def _complete_initialization(self):
        self._base_camp_coordinates = self._average(self._initialization_coordinates)
        self._initializing_gps = False

    def _measure_rocket_movement(self, utm_coordinates: UTMCoordinates):
        relative_position = utm_coordinates - self._base_camp_coordinates

        self._easting.append(relative_position.easting)
        self._northing.append(relative_position.northing)

    def _average(self, initialization_coordinates: List[UTMCoordinates]):
        return sum(initialization_coordinates, self._base_camp_coordinates) / len(initialization_coordinates)

    def get_last_coordinates(self) -> GpsCoordinates:
        return self._last_coordinates

    def get_projected_coordinates(self):
        return self._easting, self._northing

    def reset(self):
        self._easting = []
        self._northing = []
        self._initialization_coordinates = []
        self._base_camp_coordinates = UTMCoordinates(0.0, 0.0)
        self._last_coordinates = GpsCoordinates(0.0, 0.0)
        self._first_gps_fix_timestamp = None
        self._initializing_gps = True
