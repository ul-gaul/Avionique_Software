import abc
from PyQt5 import QtWidgets


class DataWidget(QtWidgets.QWidget):
    __metaclass__ = abc.ABCMeta

    def __init__(self, parent=None):
        super().__init__(parent)
