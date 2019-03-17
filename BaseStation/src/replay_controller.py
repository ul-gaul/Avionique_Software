from src.config import Config
from src.controller import Controller
from src.data_processing.consumer import Consumer
from src.replay.file_data_producer import FileDataProducer
from src.ui.replay_widget import ReplayWidget


class ReplayController(Controller):

    def __init__(self, replay_widget: ReplayWidget, file_data_producer: FileDataProducer, consumer: Consumer,
                 config: Config):
        super().__init__(replay_widget, file_data_producer, consumer, config)

        self.data_widget.set_callback("play", self.play_button_callback)
        self.data_widget.set_callback("pause", self.pause_button_callback)
        self.data_widget.set_callback("fast_forward", self.fast_forward_button_callback)
        self.data_widget.set_callback("rewind", self.rewind_button_callback)
        self.data_widget.set_control_bar_max_value(self.data_producer.get_total_packet_count() - 1)
        self.data_widget.set_control_bar_callback(self.control_bar_callback)

        self.update()

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

    def control_bar_callback(self, frame_index: int):
        self.data_producer.set_current_packet_index(frame_index)

    def activate(self, filename):  # TODO
        pass

    def deactivate(self) -> bool:
        if self.is_running:
            self.stop_thread()

        self.consumer.reset()
        self.data_widget.reset()

        return True
