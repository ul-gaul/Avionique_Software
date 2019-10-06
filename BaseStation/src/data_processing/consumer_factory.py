from src.config import Config
from src.data_processing.angular_position_calculator import AngularCalculator
from src.data_processing.angular_speed_integrator import AngularSpeedIntegrator
from src.data_processing.apogee_calculator import ApogeeCalculator
from src.data_processing.consumer import Consumer
from src.data_processing.gps.coordinate_conversion_strategy_factory import CoordinateConversionStrategyFactory
from src.data_processing.gps.gps_fix_validator import GpsFixValidatorFactory
from src.data_processing.gps.gps_initializer import GpsInitializer
from src.data_processing.gps.gps_processor import GpsProcessor
from src.data_processing.gps.utm_coordinates_converter import UTMCoordinatesConverter
from src.data_processing.orientation_processor import OrientationProcessor
from src.data_producer import DataProducer


class ConsumerFactory:
    def __init__(self, coordinate_conversion_strategy_factory: CoordinateConversionStrategyFactory,
                 gps_fix_validator_factory: GpsFixValidatorFactory):
        self.coordinate_conversion_strategy_factory = coordinate_conversion_strategy_factory
        self.gps_fix_validator_factory = gps_fix_validator_factory

    def create(self, data_producer: DataProducer, rocket_packet_version: int, config: Config) -> Consumer:
        coordinate_conversion_strategy = self.coordinate_conversion_strategy_factory.create(rocket_packet_version)
        utm_coordinates_converter = UTMCoordinatesConverter(config.gps_config.utm_zone)

        gps_fix_validator = self.gps_fix_validator_factory.create(rocket_packet_version)
        gps_initializer = GpsInitializer(config.gps_config.initialization_delay)
        gps_processor = GpsProcessor(gps_fix_validator, coordinate_conversion_strategy, utm_coordinates_converter,
                                     gps_initializer)

        angular_speed_integrator = AngularSpeedIntegrator()
        orientation_processor = OrientationProcessor(10, angular_speed_integrator)

        return Consumer(data_producer, ApogeeCalculator(), AngularCalculator(), gps_processor, orientation_processor)
