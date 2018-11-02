import threading

from src.consumer import Consumer
from src.controller import Controller
from src.file_data_producer import FileDataProducer
from src.playback_state import PlaybackState
from src.ui.replay_widget import ReplayWidget
from src.persistence.csv_data_persister import CsvDataPersister


class ReplayController(Controller):

    def __init__(self, replay_widget: ReplayWidget, filename: str):
        super().__init__(replay_widget)

        csv_data_persister = CsvDataPersister()     # FIXME: this should not be instantiated here
        data_lock = threading.Lock()
        playback_lock = threading.Lock()
        playback_state = PlaybackState(1, PlaybackState.Mode.FORWARD)
        self.data_producer = FileDataProducer(csv_data_persister, filename, data_lock, playback_lock, playback_state)

        self.consumer = Consumer(self.data_producer, self.sampling_frequency)
        self.consumer.update()

        self.data_widget.set_callback("play", self.play_button_callback)
        self.data_widget.set_callback("pause", self.pause_button_callback)
        self.data_widget.set_callback("fast_forward", self.fast_forward_button_callback)
        self.data_widget.set_callback("rewind", self.rewind_button_callback)
        self.data_widget.set_control_bar_max_value(self.data_producer.get_total_packet_count() - 1)   # TODO: unit test this interaction

        self.update_ui()

    def update_ui(self):
        super().update_ui()
        self.update_control_bar()

    def update_control_bar(self):
        self.data_widget.set_control_bar_current_value(self.data_producer.get_current_packet_index())

    def play_button_callback(self):
        self.data_producer.restart()
        if not self.is_running:
            self.start_thread()

    def pause_button_callback(self):
        self.data_producer.suspend()

    def fast_forward_button_callback(self):
        self.data_producer.fast_forward()
        self.update_replay_speed_indicator()

    def rewind_button_callback(self):
        self.data_producer.rewind()
        self.update_replay_speed_indicator()

    def update_replay_speed_indicator(self):
        self.data_widget.update_replay_speed_text(self.data_producer.get_speed())
