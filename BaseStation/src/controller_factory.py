import threading

from src.config import ConfigLoader
from src.file_data_producer import FileDataProducer
from src.persistence.csv_data_persister import CsvDataPersister
from src.playback_state import PlaybackState
from src.real_time_controller import RealTimeController
from src.replay_controller import ReplayController
from src.rocket_packet_parser_factory import RocketPacketParserFactory
from src.serial_data_producer import SerialDataProducer
from src.ui.real_time_widget import RealTimeWidget
from src.ui.replay_widget import ReplayWidget


class ControllerFactory:

    def __init__(self):
        self.csv_data_persister = CsvDataPersister()

    def create_real_time_controller(self, real_time_widget: RealTimeWidget):
        config = ConfigLoader.load()

        rocket_packet_parser = RocketPacketParserFactory.create(config.rocket_packet_config.version)
        lock = threading.Lock()
        data_producer = SerialDataProducer(
            lock, self.csv_data_persister, rocket_packet_parser,
            sampling_frequency=config.rocket_packet_config.sampling_frequency,
            start_character=config.serial_port_config.start_character,
            baudrate=config.serial_port_config.baudrate)

        return RealTimeController(real_time_widget, data_producer, config)

    def create_replay_controller(self, replay_widget: ReplayWidget, filename: str):
        config = ConfigLoader.load()

        data_lock = threading.RLock()
        playback_lock = threading.Lock()
        playback_state = PlaybackState(1, PlaybackState.Mode.FORWARD)
        data_producer = FileDataProducer(self.csv_data_persister, filename, data_lock, playback_lock, playback_state)

        return ReplayController(replay_widget, data_producer, config)
