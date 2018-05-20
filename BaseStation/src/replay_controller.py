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
        self.data_widget.set_callback("rewind", self.rewind_button_callback)
        csv_data_persister = CsvDataPersister()     # FIXME: this should not be instantiated here
        self.replay_manipulation_mutex = threading.Lock()
        self.data_producer = FileDataProducer(csv_data_persister, filename, self.replay_manipulation_mutex)
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
        self.replay_manipulation_mutex.acquire()
        if self.data_producer.is_real_speed():
            self.data_producer.set_mode_forward()
        if self.data_producer.is_going_forward():
            self.data_producer.accelerate()
        else:
            self.data_producer.decelerate()
        self.replay_manipulation_mutex.release()
        self.update_replay_speed_indicator()

    def rewind_button_callback(self):
        self.replay_manipulation_mutex.acquire()
        # todo: need to make backward production work first
        # if self.data_producer.is_real_speed():
        #     self.data_producer.set_mode_backward()
        if self.data_producer.is_going_backward():
            self.data_producer.accelerate()
        else:
            self.data_producer.decelerate()
        self.replay_manipulation_mutex.release()
        self.update_replay_speed_indicator()

    def update_replay_speed_indicator(self):
        self.data_widget.update_replay_speed_text(self.data_producer.get_speed())
