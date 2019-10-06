from src.data_processing.gps.coordinate_conversion_strategy import CoordinateConversionStrategy
from src.data_processing.gps.gps_coordinates import GpsCoordinates
from src.data_processing.gps.gps_fix_validator import GpsFixValidator
from src.data_processing.gps.gps_initializer import GpsInitializer, GpsInitializerListener
from src.data_processing.gps.utm_coordinates import UTMCoordinates
from src.data_processing.gps.utm_coordinates_converter import UTMCoordinatesConverter
from src.rocket_packet.rocket_packet import RocketPacket


class GpsProcessor(GpsInitializerListener):

    def __init__(self, gps_fix_validator: GpsFixValidator, coordinate_conversion_strategy: CoordinateConversionStrategy,
                 utm_coordinates_converter: UTMCoordinatesConverter, gps_initializer: GpsInitializer):
        self._gps_fix_validator = gps_fix_validator
        self._coordinate_conversion_strategy = coordinate_conversion_strategy
        self._utm_coordinates_converter = utm_coordinates_converter
        self._gps_initializer = gps_initializer
        self._gps_initializer.register_listener(self)
        self._easting = []
        self._northing = []
        self._base_camp_coordinates = UTMCoordinates(0.0, 0.0)
        self._last_coordinates = GpsCoordinates(0.0, 0.0)
        self._initializing_gps = True

    def update(self, rocket_packet: RocketPacket):
        if self._gps_fix_validator.is_fixed(rocket_packet):
            self._last_coordinates = self._coordinate_conversion_strategy.to_decimal_degrees(rocket_packet.latitude,
                                                                                             rocket_packet.longitude)
            utm_coordinates = self._utm_coordinates_converter.decimal_degrees_to_utm(self._last_coordinates)

            self._process_coordinates(rocket_packet.time_stamp, utm_coordinates)

    def _process_coordinates(self, timestamp: float, utm_coordinates: UTMCoordinates):
        if self._initializing_gps:
            self._gps_initializer.update(timestamp, utm_coordinates)
            self._easting.append(0)
            self._northing.append(0)
        else:
            relative_position = utm_coordinates - self._base_camp_coordinates
            self._easting.append(relative_position.easting)
            self._northing.append(relative_position.northing)

    def notify_initialization_complete(self, base_camp_coordinates: UTMCoordinates):
        self._base_camp_coordinates = base_camp_coordinates
        self._initializing_gps = False

    def get_last_coordinates(self) -> GpsCoordinates:
        return self._last_coordinates

    def get_projected_coordinates(self):
        return self._easting, self._northing

    def reset(self):
        self._easting = []
        self._northing = []
        self._base_camp_coordinates = UTMCoordinates(0.0, 0.0)
        self._last_coordinates = GpsCoordinates(0.0, 0.0)
        self._gps_initializer.reset()
        self._initializing_gps = True
