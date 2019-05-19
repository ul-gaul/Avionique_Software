from typing import Callable
from PyQt5 import QtWidgets, QtCore, QtGui

from src.ui.utils import *
from src.ui.header import Header


class HomeWidget(QtWidgets.QWidget):
    def __init__(self, real_time_callback, replay_callback, parent=None):
        super().__init__(parent)
        self.real_time_button = None
        self.real_time_callback = real_time_callback
        self.replay_button = None
        self.replay_callback = replay_callback
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("homewidget")
        self.resize(1082, 638)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")

        self.header = Header(self, 400, 200)
        self.verticalLayout.addLayout(self.header.get_layout())

        top_spacer = QtWidgets.QSpacerItem(20, 178, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(top_spacer)

        self.buttons_layout = QtWidgets.QHBoxLayout()
        self.buttons_layout.setObjectName("buttons_layout")
        left_spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.buttons_layout.addItem(left_spacer)
        self.real_time_button = self._create_button("real_time_button", self.real_time_callback)
        self.buttons_layout.addWidget(self.real_time_button)
        middle_spacer = QtWidgets.QSpacerItem(180, 20, QtWidgets.QSizePolicy.MinimumExpanding,
                                              QtWidgets.QSizePolicy.Minimum)
        self.buttons_layout.addItem(middle_spacer)
        self.replay_button = self._create_button("replay_button", self.replay_callback)
        self.buttons_layout.addWidget(self.replay_button)
        right_spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.buttons_layout.addItem(right_spacer)
        self.verticalLayout.addLayout(self.buttons_layout)

        bottom_spacer = QtWidgets.QSpacerItem(20, 178, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(bottom_spacer)

        self.footer_layout = QtWidgets.QHBoxLayout()
        self.footer_layout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.footer_layout.setObjectName("footer_layout")
        footer_spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.footer_layout.addItem(footer_spacer)
        self.footer_label = QtWidgets.QLabel(self)
        set_size_policy(self.footer_label, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        self.footer_label.setObjectName("footer_label")
        self.footer_layout.addWidget(self.footer_label)
        self.verticalLayout.addLayout(self.footer_layout)

        self.retranslateUi()

    def _create_button(self, name: str, callback: Callable[[], None]):
        button = QtWidgets.QPushButton(self)
        set_minimum_expanding_size_policy(button)
        button.setMinimumSize(QtCore.QSize(225, 180))
        button.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(16)
        button.setFont(font)
        button.setIconSize(QtCore.QSize(20, 20))
        button.setObjectName(name)
        button.clicked.connect(callback)
        return button

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("homewidget", "Form"))
        self.real_time_button.setText(_translate("homewidget", "Real Time"))
        self.replay_button.setText(_translate("homewidget", "Replay"))
        self.footer_label.setText(_translate("homewidget", "GAUL, 2017"))
