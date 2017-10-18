from BaseStation.src.ui.data_widget import DataWidget
from PyQt5.QtWidgets import QLCDNumber, QPushButton


class RealTimeWidget(DataWidget):

    def __init__(self, start_stop_button_callback, parent=None):
        super().__init__(parent)
        self.start_stop_button_callback = start_stop_button_callback
        self.start_stop_button = QPushButton(self.widget)
        self.init_button(self.start_stop_button, "start_stop_button", "Démarrer l'acquisition", self.update_button_text)

        self.lcdNumber = QLCDNumber(self.widget)
        self.set_minimum_expanding_size_policy(self.lcdNumber)
        self.lcdNumber.setObjectName("lcdNumber")
        self.horizontalLayout_5.addWidget(self.lcdNumber)

    def update_button_text(self):
        text = self.start_stop_button_callback()
        self.start_stop_button.setText(text)

    def set_time(self, time):
        self.lcdNumber.display(time)
