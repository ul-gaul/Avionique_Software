import threading

from src.consumer import Consumer
from src.controller import Controller
from src.file_data_producer import FileDataProducer
from src.ui.replay_widget import ReplayWidget
from src.persistence.csv_data_persister import CsvDataPersister


class ReplayController(Controller):

    def __init__(self, replay_widget: ReplayWidget, filename: str):
        super().__init__()
        self.data_widget = replay_widget
        self.data_widget.set_callback("play", self.play_button_callback)
        self.data_widget.set_callback("pause", self.pause_button_callback)
        self.data_widget.set_callback("fast_forward", self.fast_forward_button_callback)
        csv_data_persister = CsvDataPersister()     # FIXME: this should not be instantiated here
        self.data_producer = FileDataProducer(threading.Lock(), csv_data_persister, filename)
        self.consumer = Consumer(self.data_producer, self.sampling_frequency)
        self.consumer.update()
        self.update_plots()

    def play_button_callback(self):
        self.data_producer.restart()
        if not self.is_running:
            self.start_thread()

    def pause_button_callback(self):
        self.data_producer.suspend()

    def fast_forward_button_callback(self):
        pass
