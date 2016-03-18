from main_windowUI import Ui_MainWindow
from PyQt4 import QtCore, QtGui
import sys

from flight_data import flightData

class MainWindow(QtGui.QMainWindow,Ui_MainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self,parent)
        self.setupUI(parent)
        self.init_widgets()

    def init_widgets(self):
        self.flightDataPush.clicked.connect(self.open_flightData)

    def open_flightData(self):
        flight_data = flightData(self)

