from datetime import datetime
from enum import Enum

from PyQt5.QtWidgets import QMessageBox

from src.message_sender import MessageSender
from src.message_type import MessageType
from src.realtime.serial_data_producer import SerialDataProducer
from src.ui.real_time_widget import RealTimeWidget


class SaveStatus(Enum):
    SAVED = 0
    UNSAVED = 1
    CANCELLED = 2


class SaveManager(MessageSender):

    BASE_PATH = "./src/resources/"

    def __init__(self, serial_data_producer: SerialDataProducer, real_time_widget: RealTimeWidget):
        super().__init__()
        self.serial_data_producer = serial_data_producer
        self.real_time_widget = real_time_widget

    def save(self) -> SaveStatus:
        should_save = self.real_time_widget.show_save_message_box()

        if should_save == QMessageBox.Yes:
            filename = self._get_save_file_name()

            if filename:
                self._save_data(filename)
                return SaveStatus.SAVED
            else:
                return SaveStatus.CANCELLED
        elif should_save == QMessageBox.No:
            return SaveStatus.UNSAVED
        else:
            return SaveStatus.CANCELLED

    def _get_save_file_name(self) -> str:
        default_path = self.BASE_PATH + datetime.now().strftime("%Y-%m-%d_%Hh%Mm") + ".csv"
        return self.real_time_widget.get_save_file_name(default_path)

    def _save_data(self, filename: str):
        self.serial_data_producer.save(filename)
        message = "Données sauvegardées dans le fichier: " + filename
        self.notify_all_message_listeners(message, MessageType.INFO)
