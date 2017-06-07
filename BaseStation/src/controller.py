from threading import Thread
from src.serial_reader import SerialReader
from src.FileReader import FileReader
from src.consumer import Consumer
from src.ui.mainwindow import MainWindow


class Controller:
    def __init__(self, main_window):
        assert isinstance(main_window, MainWindow)
        self.main_window = main_window
        self.filename = ""
        self.is_running = False
        self.producer = None
        self.consumer = None
        self.thread = Thread(self.drawing_thread)

    def set_filename(self, filename):
        assert isinstance(filename, str)
        self.filename = filename

    def drawing_thread(self):
        while self.is_running:
            self.consumer.update()
            if self.consumer.has_new_data:
                # TODO: draw plots and update
                self.main_window.real_time_widget.altitude_curve.setData(self.consumer["altitude"])
                self.main_window.real_time_widget.target_altitude_line.setData([10000 for i in range(len(self.consumer["altitude"]))])
                self.consumer.has_new_data = False

    def init_real_time_mode(self):
        self.producer = SerialReader()
        self.start_thread()

    def init_replay_mode(self):
        self.producer = FileReader(self.filename)
        self.start_thread()

    def start_thread(self):
        self.consumer = Consumer(self.producer)
        self.is_running = True
        self.thread.start()

    def stop_thread(self):
        self.is_running = False
        self.thread.join()

    # TODO: add ui event processing methods here
