from src.controller import Controller
from src.ui.motor_widget import MotorWidget
from src.replay_controller import FileDataProducer
from src.data_processing.consumer_factory import ConsumerFactory
from src.config import Config
from PyQt5.QtCore.QTimer import QTimer

class MotorController(Controller):
    def __init__(self, replay_widget: MotorWidget, file_data_producer: FileDataProducer,
                 consumer_factory: ConsumerFactory, config: Config, timer: QTimer):
        super().__init__(replay_widget, file_data_producer, consumer_factory, config, timer)

        self.data_widget.set_callback("play_pause", self.play_pause_button_callback)
        self.data_widget.set_callback("fast_forward", self.fast_forward_button_callback)
        self.data_widget.set_callback("rewind", self.rewind_button_callback)
        self.data_widget.set_control_bar_callback(self.control_bar_callback)

    def activate(self, filename: str):
        self.update()

    def deactivate(self) -> bool:
        return True
