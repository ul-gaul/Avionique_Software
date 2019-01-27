import time
from threading import Thread
from PyQt5.QtGui import QCloseEvent

from src.config import Config
from src.consumer import Consumer
from src.data_producer import DataProducer
from src.domain_error import DomainError
from src.message_listener import MessageListener
from src.message_type import MessageType
from src.openrocket_simulation import OpenRocketSimulation
from src.ui.data_widget import DataWidget


# FIXME: this class should be abstract
class Controller:
    def __init__(self, data_widget: DataWidget, data_producer: DataProducer, consumer: Consumer, config: Config):
        self.data_widget = data_widget
        self.is_running = False
        self.data_producer = data_producer
        self.target_altitude = config.target_altitude
        self.sampling_frequency = config.rocket_packet_config.sampling_frequency
        self.consumer = consumer
        self.refresh_delay = 1.0 / config.gui_fps
        self.message_listeners = []
        self.thread = None

    def add_open_rocket_simulation(self, filename):
        try:
            simulation = OpenRocketSimulation(filename)
            self.data_widget.show_simulation(simulation)
            self.notify_all_message_listeners("Fichier de simulation " + filename + " chargé", MessageType.INFO)
        except DomainError as error:
            self.notify_all_message_listeners(error.message, MessageType.ERROR)

    def drawing_thread(self):
        last_time = time.time()
        while self.is_running:
            self.update()

            now = time.time()
            dt = now - last_time
            last_time = now
            if dt < self.refresh_delay:
                time.sleep(self.refresh_delay - dt)

    def update(self):   # TODO: unit test this
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
        self.data_widget.draw_altitude(self.consumer["altitude_feet"])
        self.data_widget.draw_apogee(self.consumer["apogee"])
        self.data_widget.draw_map(self.consumer["easting"], self.consumer["northing"])
        self.data_widget.draw_voltage(self.consumer["voltage"])

    def update_3d_model(self):
        self.data_widget.rotate_rocket_model(*self.consumer.get_rocket_rotation())

    def update_leds(self):
        self.data_widget.set_led_state(1, self.consumer["acquisition_board_state_1"][-1])
        self.data_widget.set_led_state(2, self.consumer["acquisition_board_state_2"][-1])
        self.data_widget.set_led_state(3, self.consumer["acquisition_board_state_3"][-1])
        self.data_widget.set_led_state(4, self.consumer["power_supply_state_1"][-1])
        self.data_widget.set_led_state(5, self.consumer["power_supply_state_2"][-1])
        self.data_widget.set_led_state(6, self.consumer["payload_board_state_1"][-1])

    def update_thermometer(self):
        self.data_widget.set_thermometer_value(self.consumer.get_average_temperature())

    def start_thread(self):
        self.data_producer.start()
        self.is_running = True
        self.thread = Thread(target=self.drawing_thread)
        print(self.thread)
        self.thread.start()

    def stop_thread(self):
        self.is_running = False
        self.thread.join()
        self.data_producer.stop()

    def on_close(self, event: QCloseEvent):
        if self.is_running:
            self.stop_thread()

        event.accept()

    def register_message_listener(self, message_listener: MessageListener):
        self.message_listeners.append(message_listener)

    def notify_all_message_listeners(self, message: str, message_type: MessageType):
        for message_listener in self.message_listeners:
            message_listener.notify(message, message_type)
