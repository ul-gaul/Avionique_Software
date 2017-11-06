from PyQt5 import QtWidgets, QtCore
from src.ui.utils import set_size_policy


class Led(QtWidgets.QWidget):

    def __init__(self, parent: QtWidgets.QWidget):
        super().__init__(parent)
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setObjectName("led_layout")

        light_bulb = QtWidgets.QPushButton(self)

        set_size_policy(light_bulb, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        light_bulb.setMinimumSize(QtCore.QSize(32, 32))
        light_bulb.setMaximumSize(QtCore.QSize(32, 32))
        light_bulb.setStyleSheet("")
        light_bulb.setText("")
        light_bulb.setObjectName("led_light_bulb")
        self.layout.addWidget(light_bulb)
        label = QtWidgets.QLabel(self)
        label.setObjectName("led_label")
        self.layout.addWidget(label)

    def get_layout(self):
        return self.layout
