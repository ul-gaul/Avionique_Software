import threading

from src.data_processing.angular_position_calculator import AngularCalculator
from src.config import ConfigLoader
from src.data_processing.apogee_calculator import ApogeeCalculator
from src.data_processing.consumer import Consumer
from src.persistence.csv_data_persister import CsvDataPersister
from src.real_time_controller import RealTimeController
from src.realtime.checksum_validator import ChecksumValidator
from src.realtime.rocket_packet_parser_factory import RocketPacketParserFactory
from src.realtime.serial_data_producer import SerialDataProducer
from src.replay.file_data_producer import FileDataProducer
from src.replay.playback_state import PlaybackState
from src.replay_controller import ReplayController
from src.ui.console_message_listener import ConsoleMessageListener
from src.ui.real_time_widget import RealTimeWidget
from src.ui.replay_widget import ReplayWidget


class ControllerFactory:

    def __init__(self):
        self.csv_data_persister = CsvDataPersister()

    def create_real_time_controller(self, real_time_widget: RealTimeWidget, console: ConsoleMessageListener):
        config = ConfigLoader.load()

        checksum_validator = ChecksumValidator()
        checksum_validator.register_message_listener(console)   # FIXME: maybe this should be done elsewhere...

        rocket_packet_parser = RocketPacketParserFactory.create(config.rocket_packet_config.version)
        lock = threading.Lock()
        data_producer = SerialDataProducer(
            lock, self.csv_data_persister, rocket_packet_parser, checksum_validator,
            sampling_frequency=config.rocket_packet_config.sampling_frequency,
            start_character=config.serial_port_config.start_character,
            baudrate=config.serial_port_config.baudrate)

        consumer = Consumer(data_producer, config.rocket_packet_config.sampling_frequency, ApogeeCalculator(), AngularCalculator(config.rocket_packet_config.sampling_frequency))

        return RealTimeController(real_time_widget, data_producer, consumer, config)

    def create_replay_controller(self, replay_widget: ReplayWidget, filename: str):
        config = ConfigLoader.load()

        data_lock = threading.RLock()
        playback_lock = threading.Lock()
        playback_state = PlaybackState(1, PlaybackState.Mode.FORWARD)
        data_producer = FileDataProducer(self.csv_data_persister, filename, data_lock, playback_lock, playback_state)

        consumer = Consumer(data_producer, config.rocket_packet_config.sampling_frequency, ApogeeCalculator(), AngularCalculator(config.rocket_packet_config.sampling_frequency))

        return ReplayController(replay_widget, data_producer, consumer, config)
