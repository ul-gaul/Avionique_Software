from PyQt5.QtGui import QCloseEvent

from src.config import Config
from src.controller import Controller
from src.data_processing.consumer_factory import ConsumerFactory
from src.domain_error import DomainError
from src.message_type import MessageType
from src.realtime.serial_data_producer import SerialDataProducer, NoConnectedDeviceException
from src.save import SaveManager, SaveStatus
from src.ui.real_time_widget import RealTimeWidget


class RealTimeController(Controller):
    def __init__(self, real_time_widget: RealTimeWidget, serial_data_producer: SerialDataProducer,
                 consumer_factory: ConsumerFactory, save_manager: SaveManager, config: Config):
        super().__init__(real_time_widget, serial_data_producer, consumer_factory, config)
        self.save_manager = save_manager

        self.data_widget.set_target_altitude(self.target_altitude)
        self.data_widget.set_button_callback(self.real_time_button_callback)

    def update_ui(self):
        super().update_ui()
        self.update_timer()

    def update_timer(self):
        self.data_widget.set_time(self.consumer["time_stamp"][-1])

    def real_time_button_callback(self):
        if not self.is_running:
            try:
                if self.data_producer.has_unsaved_data():
                    save_status = self.save_manager.save()

                    if save_status == SaveStatus.CANCELLED:
                        return

                self.data_producer.clear_rocket_packets()
                self.data_widget.reset()
                self.create_new_consumer(self.current_config.rocket_packet_config.version)

                self.start_thread()
            except (DomainError, NoConnectedDeviceException) as error:
                self.is_running = False
                self.notify_all_message_listeners(str(error), MessageType.ERROR)
        else:
            self.stop_thread()

        self.data_widget.update_button_text(self.is_running)

    def on_close(self, event: QCloseEvent):
        if self.data_producer.has_unsaved_data():
            save_status = self.save_manager.save()

            if save_status == SaveStatus.CANCELLED:
                event.ignore()
                return

        if self.is_running:
            self.stop_thread()

        event.accept()

    def activate(self, _):
        self.data_widget.update_button_text(self.is_running)

    def deactivate(self) -> bool:
        if self.data_producer.has_unsaved_data():
            save_status = self.save_manager.save()

            if save_status == SaveStatus.CANCELLED:
                return False

        if self.is_running:
            self.stop_thread()

        self.data_producer.clear_rocket_packets()
        self.data_widget.reset()

        return True
