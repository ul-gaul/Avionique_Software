from .mainwindowUI import Ui_MainWindow
from PyQt5.QtWidgets import QFileDialog, QApplication
from .data import Data
from PyQt5 import QtCore, QtGui
from datetime import datetime as d
import sys


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super().__init__(self,parent)
        self.setupUi(parent)
        self.initUI()

    def initUI(self):
        self.pushButton.clicked.connect(self.openRT)
        self.pushButton_2.clicked.connect(self.openRP)

    def openRT(self):
        """  """
        real_time_dialog = Data(self)
        real_time_dialog.exec_()
        Data.saveFileName()



    def openRP(self):
        """   """
        replay_dialog = Data(self)
        replay_dialog.exec_()
        Data.openFileName()




