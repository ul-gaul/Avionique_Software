from PyQt5 import QtWidgets, QtCore, QtGui
from src.ui.utils import set_size_policy, read_stylesheet


class Led(QtWidgets.QWidget):

    def __init__(self, parent: QtWidgets.QWidget, label_text: str):
        super().__init__(parent)
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setObjectName("led_layout")

        self.on_stylesheet = read_stylesheet("resources/led_on.css")
        self.off_stylesheet = read_stylesheet("resources/led_off.css")

        self.light_bulb = QtWidgets.QPushButton(self)
        set_size_policy(self.light_bulb, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.light_bulb.setMinimumSize(QtCore.QSize(32, 32))
        self.light_bulb.setMaximumSize(QtCore.QSize(32, 32))
        self.light_bulb.setStyleSheet("")
        self.light_bulb.setText("")
        self.light_bulb.setObjectName("led_light_bulb")
        self.layout.addWidget(self.light_bulb)

        label = QtWidgets.QLabel(self)
        label.setObjectName("led_label")
        label.setText(label_text)
        self.layout.addWidget(label)

    def get_layout(self):
        return self.layout

    def set_state(self, is_on: bool):
        if is_on:
            self.light_bulb.setStyleSheet(self.on_stylesheet)
        else:
            self.light_bulb.setStyleSheet(self.off_stylesheet)
