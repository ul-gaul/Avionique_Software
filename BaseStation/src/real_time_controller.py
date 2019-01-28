from datetime import datetime
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QMessageBox

from src.config import Config
from src.consumer import Consumer
from src.ui.real_time_widget import RealTimeWidget
from src.controller import Controller
from src.domain_error import DomainError
from src.message_type import MessageType
from src.serial_data_producer import SerialDataProducer


class RealTimeController(Controller):
    def __init__(self, real_time_widget: RealTimeWidget, serial_data_producer: SerialDataProducer, consumer: Consumer,
                 config: Config):
        super().__init__(real_time_widget, serial_data_producer, consumer, config)

        self.data_widget.set_target_altitude(self.target_altitude)
        self.data_widget.set_button_callback(self.real_time_button_callback)

    def update_ui(self):
        super().update_ui()
        self.update_timer()

    def update_timer(self):
        self.data_widget.set_time(self.consumer["time_stamp"][-1] / float(self.sampling_frequency))

    def real_time_button_callback(self):
        if not self.is_running:
            try:
                if self.data_producer.has_unsaved_data():
                    should_save = self.data_widget.show_save_message_box()

                    if should_save == QMessageBox.Yes:
                        filename = self.get_save_file_name()

                        if filename:
                            self.save_data(filename)
                        else:
                            return
                    elif should_save == QMessageBox.Cancel:
                        return

                    self.consumer.reset()
                    self.data_widget.reset()

                self.start_thread()
            except DomainError as error:    # TODO: test this
                self.is_running = False
                self.notify_all_message_listeners(error.message, MessageType.ERROR)
        else:
            self.stop_thread()

        self.data_widget.update_button_text(self.is_running)

    def on_close(self, event: QCloseEvent):
        if self.is_running:
            self.stop_thread()

        if self.data_producer.has_unsaved_data():
            should_save = self.data_widget.show_save_message_box()

            if should_save == QMessageBox.Yes:
                filename = self.get_save_file_name()

                if filename:
                    self.save_data(filename)
                    event.accept()
                else:
                    event.ignore()
            elif should_save == QMessageBox.No:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

    def get_save_file_name(self) -> str:
        default_path = "./src/resources/" + datetime.now().strftime("%Y-%m-%d_%Hh%Mm") + ".csv"
        return self.data_widget.get_save_file_name(default_path)

    def save_data(self, filename: str):
        self.data_producer.save(filename)
        message = "Données sauvegardées dans le fichier: " + filename
        self.notify_all_message_listeners(message, MessageType.INFO)
