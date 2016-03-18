from main_windowUI import Ui_MainWindow
from PyQt4 import QtCore, QtGui
import sys

class MainWindow(QtGui.QMainWindow,Ui_MainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self,parent)
        self.setupUI(parent)
        self.init_widgets()

    def init_widgets(self):
        self.pushButton

    def open_flight_data(self):
