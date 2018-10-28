import time
from threading import Thread
from PyQt5.QtGui import QCloseEvent

from src.consumer import Consumer
from src.domain_error import DomainError
from src.message_listener import MessageListener
from src.message_type import MessageType
from src.openrocket_simulation import OpenRocketSimulation
from src.ui.data_widget import DataWidget


# FIXME: this class should be abstract
class Controller:
    def __init__(self, data_widget: DataWidget, frame_per_second: float = 10.0):
        self.data_widget = data_widget
        self.is_running = False
        self.data_producer = None
        self.consumer = None
        self.target_altitude = 10000
        self.sampling_frequency = 1
        self.refresh_delay = 1.0 / frame_per_second
        self.ui_update_functions = [self.update_plots, self.update_leds, self.update_thermometer, self.update_3d_model]
        self.message_listeners = []
        self.thread = Thread(target=self.drawing_thread)

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
            self.consumer.update()

            if self.consumer.has_data():
                self.call_ui_update_functions()

            self.consumer.clear()

            now = time.time()
            dt = now - last_time
            last_time = now
            if dt < self.refresh_delay:
                time.sleep(self.refresh_delay - dt)

    def update_plots(self):
        self.data_widget.draw_altitude(self.consumer["altitude_feet"])
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

    def call_ui_update_functions(self):
        for function in self.ui_update_functions:
            function()

    def start_thread(self):
        self.consumer = Consumer(self.data_producer, self.sampling_frequency)
        self.data_producer.start()
        self.is_running = True
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
