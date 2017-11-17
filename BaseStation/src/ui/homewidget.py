from typing import Callable
from PyQt5 import QtWidgets, QtCore, QtGui

from src.ui.utils import *


class HomeWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.real_time_button = None
        self.replay_button = None
        self.setup_ui()
        self.label.setPixmap(QtGui.QPixmap("resources/logo.jpg"))

    def setup_ui(self):
        self.setObjectName("homewidget")
        self.resize(1082, 638)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(30, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label = QtWidgets.QLabel(self)
        set_minimum_size_policy(self.label)
        self.label.setMinimumSize(QtCore.QSize(0, 0))
        self.label.setMaximumSize(QtCore.QSize(400, 200))
        self.label.setText("")
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)

        spacerItem2 = QtWidgets.QSpacerItem(20, 178, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.real_time_button = self._create_button("real_time_button", self.parent().open_real_time)
        self.horizontalLayout_2.addWidget(self.real_time_button)
        spacerItem4 = QtWidgets.QSpacerItem(180, 20, QtWidgets.QSizePolicy.MinimumExpanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.replay_button = self._create_button("replay_button", self.parent().open_replay)
        self.horizontalLayout_2.addWidget(self.replay_button)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem5)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        spacerItem6 = QtWidgets.QSpacerItem(20, 178, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem6)

        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem7)
        self.label_2 = QtWidgets.QLabel(self)
        set_size_policy(self.label_2, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

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
        self.label_2.setText(_translate("homewidget", "GAUL, 2017"))
