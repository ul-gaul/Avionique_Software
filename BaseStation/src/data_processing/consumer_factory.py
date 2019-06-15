from src.config import Config
from src.data_processing.angular_position_calculator import AngularCalculator
from src.data_processing.apogee_calculator import ApogeeCalculator
from src.data_processing.consumer import Consumer
from src.data_processing.gps.coordinate_conversion_strategy_factory import CoordinateConversionStrategyFactory
from src.data_producer import DataProducer


class ConsumerFactory:
    def __init__(self, coordinate_conversion_strategy_factory: CoordinateConversionStrategyFactory):
        self.coordinate_conversion_strategy_factory = coordinate_conversion_strategy_factory

    def create(self, data_producer: DataProducer, rocket_packet_version: int, config: Config) -> Consumer:
        coordinate_conversion_strategy = self.coordinate_conversion_strategy_factory.create(rocket_packet_version,
                                                                                            config.gps_config)

        return Consumer(data_producer, ApogeeCalculator(), AngularCalculator(), coordinate_conversion_strategy)
