import abc

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QCloseEvent

from src.config import Config
from src.data_processing.consumer_factory import ConsumerFactory
from src.data_producer import DataProducer
from src.message_sender import MessageSender
from src.message_type import MessageType
from src.openrocket_simulation import OpenRocketSimulation, InvalidOpenRocketSimulationFileException
from src.ui.data_widget import DataWidget


class Controller(MessageSender):
    __metaclass__ = abc.ABCMeta

    def __init__(self, data_widget: DataWidget, data_producer: DataProducer, consumer_factory: ConsumerFactory,
                 config: Config, timer: QTimer):
        super().__init__()
        self.data_widget = data_widget
        self.is_running = False
        self.data_producer = data_producer
        self.target_altitude = config.target_altitude
        self.consumer = None
        self.consumer_factory = consumer_factory
        self.updates_interval_in_millis = 1000.0 / config.gui_fps
        self.current_config = config
        self.timer = timer
        self.timer.timeout.connect(self.update)

    def add_open_rocket_simulation(self, filename):
        try:
            simulation = OpenRocketSimulation(filename)
            self.data_widget.show_simulation(simulation)
            self.notify_all_message_listeners("Fichier de simulation " + filename + " chargé", MessageType.INFO)
        except InvalidOpenRocketSimulationFileException as error:
            self.notify_all_message_listeners(str(error), MessageType.ERROR)

    def update(self):
        self.consumer.update()

        if self.consumer.has_data():
            self.update_ui()

        self.consumer.clear()

    def update_ui(self):
        self.update_plots()
        self.update_leds()
        self.update_thermometer()
        self.update_3d_model()

    def update_plots(self):
        self.data_widget.draw_altitude(self.consumer["time_stamp"], self.consumer["altitude_feet"])
        self.data_widget.draw_apogee(self.consumer["apogee"])
        self.data_widget.draw_map(*self.consumer.get_projected_coordinates())
        self.data_widget.show_current_coordinates(self.consumer.get_last_gps_coordinates())
        self.data_widget.draw_voltage(self.consumer["voltage"])

    def update_3d_model(self):
        self.data_widget.set_rocket_model_orientation(self.consumer.get_rocket_orientation())

    def update_leds(self):
        self.data_widget.set_led_state(1, self.consumer["acquisition_board_state_1"][-1])
        self.data_widget.set_led_state(2, self.consumer["acquisition_board_state_2"][-1])
        self.data_widget.set_led_state(3, self.consumer["acquisition_board_state_3"][-1])
        self.data_widget.set_led_state(4, self.consumer["power_supply_state_1"][-1])
        self.data_widget.set_led_state(5, self.consumer["power_supply_state_2"][-1])
        self.data_widget.set_led_state(6, self.consumer["payload_board_state_1"][-1])

    def update_thermometer(self):
        self.data_widget.set_thermometer_value(self.consumer.get_average_temperature())

    def start_updates(self):
        self.data_producer.start()
        self.is_running = True
        self.timer.start(self.updates_interval_in_millis)

    def stop_updates(self):
        self.is_running = False
        self.timer.stop()
        self.data_producer.stop()

    def on_close(self, event: QCloseEvent):
        if self.is_running:
            self.stop_updates()

        event.accept()

    def create_new_consumer(self, rocket_packet_version: int):
        self.consumer = self.consumer_factory.create(self.data_producer, rocket_packet_version, self.current_config)

    @abc.abstractmethod
    def activate(self, filename: str) -> None:
        """
        Prepare the controller before its thread can be started. This method should be used for process-specific setup.
        This is needed because controllers are not destroyed between processes, only activated/deactivated.
        :param filename: The name of the flight data file loaded in replay mode. Not used in real time.
        """
        pass

    @abc.abstractmethod
    def deactivate(self) -> bool:
        """
        Stop all threads and leave the software in a safe state before closing or switching mode.
        :return: A boolean that tells if the controller was deactivated successfully.
        """
        pass
