from src.controller import Controller
from src.events.event_observer import EventObserver
from src.ui.motor_widget import MotorWidget
from src.replay_controller import FileDataProducer
from src.data_processing.consumer_factory import ConsumerFactory
from src.config import Config
from PyQt5.QtCore import QTimer
from src.realtime.serial_command_sender import SerialCommandSender


class MotorController(EventObserver):
    # def __init__(self, motor_widget: MotorWidget, file_data_producer: FileDataProducer,
    #              consumer_factory: ConsumerFactory, config: Config, timer: QTimer,
    #              serial_command_sender: SerialCommandSender):
        #super().__init__(motor_widget, file_data_producer, consumer_factory, config, timer)
    def __init__(self, motor_widget: MotorWidget, serial_command_sender: SerialCommandSender):
        EventObserver.__init__(self)

        self.observe("on_command_receive", self.on_command_receive)

        self.data_widget = motor_widget
        self.command_sender = serial_command_sender
        self.command_sender.start()

        self.data_widget.set_callback("send_cmd_valve_1", lambda: self.send_command_valve_callback(1, 2, 3, 4, 5, 6, 7))
        self.data_widget.set_callback("send_cmd_valve_2", lambda: self.send_command_valve_callback(2, 2, 3, 4, 5, 6, 7))
        self.data_widget.set_callback("send_cmd_valve_3", lambda: self.send_command_valve_callback(3, 2, 3, 4, 5, 6, 7))
        self.data_widget.set_callback("send_cmd_valve_4", lambda: self.send_command_valve_callback(4, 2, 3, 4, 5, 6, 7))
        self.data_widget.set_callback("send_cmd_valve_5", lambda: self.send_command_valve_callback(5, 2, 3, 4, 5, 6, 7))

    def send_command_valve_callback(self, *args):
        self.command_sender.send_command(*args)

    def on_command_receive(self, *args):
        cmd_id = args[0]
        ack_nack = args[1]
        button = self.data_widget.getButtonByCommandID(cmd_id)

        if ack_nack == 1:
            self.data_widget.set_valve_pushButton_on(button)
        else:
            self.data_widget.set_valve_pushButton_off(button)
