from PyQt5 import QtWidgets, QtCore, QtGui
from src.ui.utils import set_minimum_size_policy


class Header(QtWidgets.QWidget):
    
    def __init__(self, parent: QtWidgets.QWidget, label_width: int, label_height: int):
        super().__init__(parent)
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setObjectName("header_layout")
        left_spacer_item = QtWidgets.QSpacerItem(30, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.layout.addItem(left_spacer_item)
        
        self.label = QtWidgets.QLabel(parent)
        set_minimum_size_policy(self.label)
        self.label.setMinimumSize(QtCore.QSize(0, 0))
        self.label.setMaximumSize(QtCore.QSize(label_width, label_height))
        self.label.setText("")
        self.label.setScaledContents(True)
        self.label.setObjectName("header_label")
        self.label.setPixmap(QtGui.QPixmap("src/resources/logo.jpg"))
        self.layout.addWidget(self.label)
        right_spacer_item = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                                  QtWidgets.QSizePolicy.Minimum)
        self.layout.addItem(right_spacer_item)

    def get_layout(self):
        return self.layout
