from src.data_processing.gps.coordinate_conversion_strategy import CoordinateConversionStrategy
from src.data_processing.gps.decimal_degrees_coordinate_conversion_strategy import \
    DecimalDegreesCoordinateConversionStrategy
from src.data_processing.gps.degree_decimal_minutes_coordinate_conversion_strategy import \
    DegreeDecimalMinutesCoordinateConversionStrategy


class CoordinateConversionStrategyFactory:

    @staticmethod
    def create(rocket_packet_version: int) -> CoordinateConversionStrategy:
        # TODO: handle invalid version
        if rocket_packet_version == 2017 or rocket_packet_version == 2018:
            return DecimalDegreesCoordinateConversionStrategy()
        elif rocket_packet_version == 2019:
            return DegreeDecimalMinutesCoordinateConversionStrategy()
