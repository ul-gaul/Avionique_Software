import threading

from PyQt5.QtCore import QTimer

from src.config import ConfigLoader
from src.data_processing.consumer_factory import ConsumerFactory
from src.data_processing.gps.coordinate_conversion_strategy_factory import CoordinateConversionStrategyFactory
from src.data_processing.gps.gps_fix_validator import GpsFixValidatorFactory
from src.persistence.csv_data_persister import CsvDataPersister
from src.real_time_controller import RealTimeController
from src.realtime.checksum_validator import ChecksumValidator
from src.realtime.serial_data_producer import SerialDataProducer
from src.realtime.serial_command_sender import SerialCommandSender
from src.replay.file_data_producer import FileDataProducer
from src.replay.playback_state import PlaybackState
from src.replay_controller import ReplayController
from src.rocket_packet.rocket_packet_parser_factory import RocketPacketParserFactory
from src.rocket_packet.rocket_packet_repository import RocketPacketRepository
from src.save import SaveManager
from src.ui.console_message_listener import ConsoleMessageListener
from src.ui.motor_widget import MotorWidget
from src.ui.real_time_widget import RealTimeWidget
from src.ui.replay_widget import ReplayWidget


class ControllerFactory:
    def __init__(self):
        self.csv_data_persister = CsvDataPersister()
        self.rocket_packet_parser_factory = RocketPacketParserFactory()
        self.rocket_packet_repository = RocketPacketRepository(self.csv_data_persister,
                                                               self.rocket_packet_parser_factory)
        self.coordinate_conversion_strategy_factory = CoordinateConversionStrategyFactory()
        self.gps_fix_validator_factory = GpsFixValidatorFactory()

    def create_real_time_controller(self, real_time_widget: RealTimeWidget, motor_widget: MotorWidget, console: ConsoleMessageListener):
        config = ConfigLoader.load()

        checksum_validator = ChecksumValidator()
        checksum_validator.register_message_listener(console)  # FIXME: maybe this should be done elsewhere...

        rocket_packet_parser = self.rocket_packet_parser_factory.create(config.rocket_packet_config.version)
        lock = threading.Lock()
        data_producer = SerialDataProducer(lock, self.rocket_packet_repository, rocket_packet_parser,
                                           checksum_validator,
                                           sampling_frequency=config.rocket_packet_config.sampling_frequency)

        consumer_factory = ConsumerFactory(self.coordinate_conversion_strategy_factory, self.gps_fix_validator_factory)

        save_manager = SaveManager(data_producer, real_time_widget)

        serial_command_sender = SerialCommandSender("COM4", 9600, "bbbbbbb")

        return RealTimeController(real_time_widget, motor_widget, data_producer, consumer_factory, save_manager, config, QTimer(),
                                  serial_command_sender)

    def create_replay_controller(self, replay_widget: ReplayWidget, motor_widget: MotorWidget):
        config = ConfigLoader.load()

        data_lock = threading.RLock()
        playback_lock = threading.Lock()
        playback_state = PlaybackState(1, PlaybackState.Mode.FORWARD)
        data_producer = FileDataProducer(self.rocket_packet_repository, data_lock, playback_lock, playback_state)

        consumer_factory = ConsumerFactory(self.coordinate_conversion_strategy_factory, self.gps_fix_validator_factory)

        return ReplayController(replay_widget, motor_widget, data_producer, consumer_factory, config, QTimer())
