from threading import Thread
import time
from PyQt5 import QtWidgets
from BaseStation.src.serial_reader import SerialReader
from BaseStation.src.FileReader import FileReader
from BaseStation.src.consumer import Consumer
from BaseStation.src.ui.real_time_widget import RealTimeWidget
from BaseStation.src.ui.replay_widget import ReplayWidget


class Controller:
    def __init__(self):
        self.data_widget = None
        self.filename = ""
        self.is_running = False
        self.producer = None
        self.consumer = None
        self.target_altitude = 10000
        self.sampling_frequency = 1
        self.fps = 0
        self.thread = Thread(target=self.drawing_thread)

    def set_filename(self, filename):
        assert isinstance(filename, str)
        self.filename = filename

    def drawing_thread(self):
        last_time = time.time()
        while self.is_running:
            self.consumer.update()
            if self.consumer.has_new_data:
                self.draw_plots()
                self.update_leds()
                self.update_thermometer()
                self.update_timer()
                self.consumer.has_new_data = False
                now = time.time()
                dt = now - last_time
                last_time = now
                QtWidgets.QApplication.processEvents()
                if dt < 1.0 / self.sampling_frequency:
                    time.sleep(1.0 / self.sampling_frequency - dt)

    def draw_plots(self):
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

    def update_timer(self):
        self.data_widget.set_time(self.consumer["time_stamp"][-1] / float(self.sampling_frequency))

    def init_real_time_mode(self, real_time_widget, save_file_path):
        assert isinstance(real_time_widget, RealTimeWidget)
        self.data_widget = real_time_widget
        self.data_widget.set_target_altitude(self.target_altitude)
        self.producer = SerialReader(sampling_frequency=self.sampling_frequency, save_file_path=save_file_path)

    def init_replay_mode(self, replay_widget):
        assert isinstance(replay_widget, ReplayWidget)
        self.data_widget = replay_widget
        self.producer = FileReader(self.filename)
        self.consumer = Consumer(self.producer, self.sampling_frequency)
        self.consumer.update()
        self.draw_plots()

    def real_time_button_callback(self):
        self.is_running = not self.is_running
        if self.is_running:
            self.start_thread()
            button_string = "Arrêter l'acquisition"
        else:
            self.stop_thread()
            button_string = "Démarrer l'acquisition"
        return button_string

    def start_thread(self):
        self.consumer = Consumer(self.producer, self.sampling_frequency)
        #self.consumer.led_callback = self.data_widget.set_led_state
        self.producer.start()
        self.is_running = True
        self.thread.start()

    def stop_thread(self):
        self.is_running = False
        self.thread.join()
        self.producer.stop()

    # TODO: add ui event processing methods here
