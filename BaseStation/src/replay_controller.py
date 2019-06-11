from src.config import Config
from src.controller import Controller
from src.data_processing.consumer_factory import ConsumerFactory
from src.replay.file_data_producer import FileDataProducer
from src.ui.replay_widget import ReplayWidget


class ReplayController(Controller):
    def __init__(self, replay_widget: ReplayWidget, file_data_producer: FileDataProducer,
                 consumer_factory: ConsumerFactory, config: Config):
        super().__init__(replay_widget, file_data_producer, consumer_factory, config)

        self.data_widget.set_callback("play_pause", self.play_pause_button_callback)
        self.data_widget.set_callback("fast_forward", self.fast_forward_button_callback)
        self.data_widget.set_callback("rewind", self.rewind_button_callback)
        self.data_widget.set_control_bar_callback(self.control_bar_callback)

    def update_ui(self):
        super().update_ui()
        self.update_control_bar()

    def update_control_bar(self):
        self.data_widget.set_control_bar_current_value(self.data_producer.get_current_packet_index())

    def play_pause_button_callback(self):
        if self.data_producer.is_suspended():
            self._play()
        else:
            self._pause()

    def _play(self):
        self.data_producer.restart()
        if not self.is_running:
            self.start_thread()
        self.data_widget.set_pause_button_text()

    def _pause(self):
        self.data_producer.suspend()
        self.data_widget.set_play_button_text()

    def fast_forward_button_callback(self):
        self.data_producer.fast_forward()
        self.update_replay_speed_indicator()

    def rewind_button_callback(self):
        self.data_producer.rewind()
        self.update_replay_speed_indicator()

    def update_replay_speed_indicator(self):
        self.data_widget.update_replay_speed_text(self.data_producer.get_speed())

    def control_bar_callback(self, frame_index: int):
        self.data_producer.set_current_packet_index(frame_index)

    def activate(self, filename: str):
        self.data_producer.load(filename)
        self.data_producer.reset_playback_state()

        self.create_new_consumer(self.data_producer.get_rocket_packet_version())

        self.data_widget.set_control_bar_max_value(self.data_producer.get_total_packet_count() - 1)
        self.data_widget.set_play_button_text()

        self.update()

    def deactivate(self) -> bool:
        if self.is_running:
            self.stop_thread()

        self.data_widget.reset()

        return True
