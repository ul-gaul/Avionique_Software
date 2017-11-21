from src.domain_error import DomainError
from src.ui.data_widget import DataWidget
from src.ui.utils import set_minimum_expanding_size_policy
from PyQt5.QtWidgets import QLCDNumber, QPushButton


class RealTimeWidget(DataWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.main_window = parent
        self.start_stop_button_callback = lambda: False
        self.start_stop_button = QPushButton(self.widget)
        self.init_button(self.start_stop_button, "start_stop_button", "Démarrer l'acquisition", self.update_button_text)

        self.lcdNumber = QLCDNumber(self.widget)
        set_minimum_expanding_size_policy(self.lcdNumber)
        self.lcdNumber.setObjectName("lcdNumber")
        self.controls_inner_layout.addWidget(self.lcdNumber)

    def set_button_callback(self, start_stop_button_callback):
        self.start_stop_button_callback = start_stop_button_callback

    def update_button_text(self):
        try:
            controller_is_running = self.start_stop_button_callback()
            if controller_is_running:
                self.start_stop_button.setText("Arrêter l'acquisition")
            else:
                self.start_stop_button.setText("Démarrer l'acquisition")
        except DomainError as e:
            self.main_window.notify(e)

    def set_time(self, time):
        self.lcdNumber.display(time)
