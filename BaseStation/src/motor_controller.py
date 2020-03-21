from src.controller import Controller
from src.ui.motor_widget import MotorWidget
from src.replay_controller import FileDataProducer
from src.data_processing.consumer_factory import ConsumerFactory
from src.config import Config
from PyQt5.QtCore import QTimer
from src.realtime.serial_command_sender import SerialCommandSender


class MotorController(Controller):
    def __init__(self, motor_widget: MotorWidget, file_data_producer: FileDataProducer,
                 consumer_factory: ConsumerFactory, config: Config, timer: QTimer,
                 serial_command_sender: SerialCommandSender):
        super().__init__(motor_widget, file_data_producer, consumer_factory, config, timer)

        self.command_sender = serial_command_sender

        self.data_widget.set_callback("send_cmd_valve_1", lambda: self.send_command_valve_callback(""))
        self.data_widget.set_callback("send_cmd_valve_2", lambda: self.send_command_valve_callback(""))
        self.data_widget.set_callback("send_cmd_valve_3", lambda: self.send_command_valve_callback(""))
        self.data_widget.set_callback("send_cmd_valve_4", lambda: self.send_command_valve_callback(""))
        self.data_widget.set_callback("send_cmd_valve_5", lambda: self.send_command_valve_callback(""))

    def send_command_valve_callback(self, *args):
        print("Command sent!")
        self.command_sender.send_command(args)

    def update_ui(self):
        super().update_ui()

    def activate(self, filename: str):
        self.update()

    def deactivate(self) -> bool:
        return True
