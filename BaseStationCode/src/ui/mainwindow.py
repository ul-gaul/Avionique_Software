from .mainwindowUI import Ui_MainWindow
from PyQt5.QtWidgets import QFileDialog, QApplication, QMainWindow
from .data import Data
from PyQt5 import QtCore, QtGui


class MainWindow(Ui_MainWindow):

    def __init__(self, main_window):
        self.main_window = main_window
        self.setupUi(self.main_window)
        self.initUI()

    def initUI(self):
        self.label.setPixmap(QtGui.QPixmap("ui/logo.jpg"))
        self.pushButton.clicked.connect(self.openRT)
        self.pushButton_2.clicked.connect(self.openRP)

    def openRT(self):
        """  """
        real_time_dialog = Data(self.main_window)
        real_time_dialog.saveFileName()


    def openRP(self):
        """   """
        replay_dialog = Data(self.main_window)
        replay_dialog.openFileName()




