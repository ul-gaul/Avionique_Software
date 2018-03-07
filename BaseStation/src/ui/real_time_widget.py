from src.ui.data_widget import DataWidget
from src.ui.utils import set_minimum_expanding_size_policy
from PyQt5.QtWidgets import QLCDNumber, QPushButton


class RealTimeWidget(DataWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.start_stop_button_callback = lambda: False
        self.start_stop_button = QPushButton(self.widget)
        self.init_button(self.start_stop_button, "start_stop_button", "Démarrer l'acquisition", self.on_button_click)

        self.lcdNumber = QLCDNumber(self.widget)
        set_minimum_expanding_size_policy(self.lcdNumber)
        self.lcdNumber.setObjectName("lcdNumber")
        self.controls_inner_layout.addWidget(self.lcdNumber)

    def set_button_callback(self, start_stop_button_callback):
        self.start_stop_button_callback = start_stop_button_callback

    def on_button_click(self):
        controller_is_running = self.start_stop_button_callback()
        self.update_button_text(controller_is_running)

    def update_button_text(self, is_acquisition_running: bool):
        if is_acquisition_running:
            self.start_stop_button.setText("Arrêter l'acquisition")
        else:
            self.start_stop_button.setText("Démarrer l'acquisition")

    def set_time(self, time):
        self.lcdNumber.display(time)
