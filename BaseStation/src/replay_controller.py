from src.consumer import Consumer
from src.controller import Controller
from src.file_data_producer import FileDataProducer
from src.ui.replay_widget import ReplayWidget
from src.persistence.csv_data_persister import CsvDataPersister


class ReplayController(Controller):

    def __init__(self, replay_widget: ReplayWidget, filename: str):
        super().__init__()
        self.data_widget = replay_widget
        csv_data_persister = CsvDataPersister()     # FIXME: this should not be instantiated here
        self.data_producer = FileDataProducer(csv_data_persister, filename)
        self.consumer = Consumer(self.data_producer, self.sampling_frequency)
        self.consumer.update()
        self.update_plots()
