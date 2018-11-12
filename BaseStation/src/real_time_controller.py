import threading
from datetime import datetime
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QMessageBox, QFileDialog

from src.config import ConfigLoader
from src.rocket_packet_parser_factory import RocketPacketParserFactory
from src.ui.real_time_widget import RealTimeWidget
from src.controller import Controller
from src.domain_error import DomainError
from src.message_type import MessageType
from src.serial_data_producer import SerialDataProducer
from src.persistence.csv_data_persister import CsvDataPersister


class RealTimeController(Controller):

    def __init__(self, real_time_widget: RealTimeWidget):
        super().__init__(real_time_widget)
        self.data_widget.set_target_altitude(self.target_altitude)
        self.data_widget.set_button_callback(self.real_time_button_callback)

        csv_data_persister = CsvDataPersister()   # FIXME: this should not be instantiated here
        config = ConfigLoader.load()
        rocket_packet_parser = RocketPacketParserFactory.create(config.rocket_packet_version)
        self.data_producer = SerialDataProducer(threading.Lock(), csv_data_persister, rocket_packet_parser,
                                                sampling_frequency=self.sampling_frequency)

    def update_ui(self):
        super().update_ui()
        self.update_timer()

    def update_timer(self):
        self.data_widget.set_time(self.consumer["time_stamp"][-1] / float(self.sampling_frequency))

    def real_time_button_callback(self):
        self.is_running = not self.is_running
        if self.is_running:
            try:
                self.start_thread()
            except DomainError as error:
                self.is_running = not self.is_running
                self.notify_all_message_listeners(error.message, MessageType.ERROR)
        else:
            self.stop_thread()
        self.data_widget.update_button_text(self.is_running)

    def on_close(self, event: QCloseEvent):
        # FIXME: clean this up then add unit tests (also this should probably go in a UI class)
        if self.is_running:
            self.stop_thread()

        if self.data_producer.has_unsaved_data():
            message_box = QMessageBox()
            should_save = message_box.question(self.data_widget, "BaseStation",
                                               "Vous avez des données non sauvegardées.\nVoulez-vous les sauvegarder?",
                                               QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Yes)
            if should_save == QMessageBox.Yes:
                placeholder_path = "./src/resources/" + datetime.now().strftime("%Y-%m-%d_%Hh%Mm") + ".csv"
                filename, _ = QFileDialog.getSaveFileName(caption="Save File", directory=placeholder_path,
                                                          filter="All Files (*);; CSV Files (*.csv)")
                if filename == "":
                    event.ignore()
                else:
                    self.data_producer.save(filename)
                    message = "Données sauvegardées dans le fichier: " + filename
                    self.notify_all_message_listeners(message, MessageType.INFO)
                    event.accept()
            elif should_save == QMessageBox.No:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()
