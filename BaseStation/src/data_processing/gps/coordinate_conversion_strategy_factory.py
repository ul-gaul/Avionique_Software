from src.config import GpsConfig
from src.data_processing.gps.coordinate_conversion_strategy import CoordinateConversionStrategy
from src.data_processing.gps.decimal_degrees_coordinate_conversion_strategy import \
    DecimalDegreesCoordinateConversionStrategy
from src.data_processing.gps.degree_decimal_minutes_coordinate_conversion_strategy import \
    DegreeDecimalMinutesCoordinateConversionStrategy
from src.data_processing.gps.utm_coordinates_converter import UTMCoordinatesConverter


class CoordinateConversionStrategyFactory:

    @staticmethod
    def create(rocket_packet_version: int, gps_config: GpsConfig) -> CoordinateConversionStrategy:
        # TODO: handle invalid version
        utm_coordinates_converter = UTMCoordinatesConverter(gps_config.utm_zone)

        if rocket_packet_version == 2017 or rocket_packet_version == 2018:
            return DecimalDegreesCoordinateConversionStrategy(utm_coordinates_converter)
        elif rocket_packet_version == 2019:
            return DegreeDecimalMinutesCoordinateConversionStrategy(utm_coordinates_converter)
