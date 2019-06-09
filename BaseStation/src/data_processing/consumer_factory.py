from src.config import Config
from src.data_processing.angular_position_calculator import AngularCalculator
from src.data_processing.apogee_calculator import ApogeeCalculator
from src.data_processing.consumer import Consumer
from src.data_producer import DataProducer


class ConsumerFactory:
    def __init__(self):
        pass

    def create(self, data_producer: DataProducer, config: Config) -> Consumer:
        return Consumer(data_producer, config.rocket_packet_config.sampling_frequency, ApogeeCalculator(),
                        AngularCalculator(config.rocket_packet_config.sampling_frequency))
