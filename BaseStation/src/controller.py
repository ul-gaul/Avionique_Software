from threading import Thread
import time
from PyQt5.QtWidgets import QApplication, QStackedWidget
from PyQt5.QtGui import QCloseEvent

from src.consumer import Consumer
from src.openrocketsimulation import OpenRocketSimulation


# FIXME: this class should be abstract
class Controller:
    def __init__(self):
        self.data_widget = None
        self.is_running = False
        self.data_producer = None
        self.consumer = None
        self.target_altitude = 10000
        self.sampling_frequency = 1
        self.fps = 0
        self.ui_update_functions = [self.update_plots, self.update_leds, self.update_thermometer]
        self.thread = Thread(target=self.drawing_thread)

    def add_open_rocket_simulation(self, filename):
        simulation = OpenRocketSimulation(filename)
        self.data_widget.show_simulation(simulation)

    def drawing_thread(self):
        last_time = time.time()
        while self.is_running:
            self.consumer.update()
            if self.consumer.has_new_data:
                self.call_ui_update_functions()
                self.consumer.has_new_data = False
                now = time.time()
                dt = now - last_time
                last_time = now
                QApplication.processEvents()
                if dt < 1.0 / self.sampling_frequency:
                    time.sleep(1.0 / self.sampling_frequency - dt)

    def update_plots(self):
        # TODO: draw plots and update
        self.data_widget.draw_altitude(self.consumer["altitude_feet"])
        self.data_widget.draw_map(self.consumer["easting"], self.consumer["northing"])
        self.data_widget.rotate_rocket_model(*self.consumer.get_rocket_rotation())

    def update_leds(self):
        # FIXME: optimize this by updating the leds only on status change
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
        #self.consumer.led_callback = self.data_widget.set_led_state
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
