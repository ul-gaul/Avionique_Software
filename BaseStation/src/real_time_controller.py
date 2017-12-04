from src.ui.real_time_widget import RealTimeWidget
from src.controller import Controller
from src.serial_reader import SerialReader
from src.domain_error import DomainError


class RealTimeController(Controller):

    def __init__(self, real_time_widget: RealTimeWidget, save_file_path: str):
        super().__init__()
        self.data_widget = real_time_widget
        self.data_widget.set_target_altitude(self.target_altitude)
        self.producer = SerialReader(sampling_frequency=self.sampling_frequency, save_file_path=save_file_path)
        self.ui_update_functions.append(self.update_timer)

    def update_timer(self):
        self.data_widget.set_time(self.consumer["time_stamp"][-1] / float(self.sampling_frequency))

    def real_time_button_callback(self):
        # FIXME: this brakes the command query separation principle
        self.is_running = not self.is_running
        if self.is_running:
            try:
                self.start_thread()
            except DomainError:
                self.is_running = not self.is_running
                raise
        else:
            self.stop_thread()
        return self.is_running