from .mainwindowUI import Ui_MainWindow
from PyQt5.QtWidgets import QFileDialog, QApplication, QMainWindow
from src.ui.data import Data
from src.ui.dataRT import DataRT
from PyQt5.QtGui import QIcon, QPixmap


class MainWindow(Ui_MainWindow):

    def __init__(self, main_window):
        self.main_window = main_window
        self.setupUi(self.main_window)
        self.initUI()

    def initUI(self):
        """  """
        self.main_window.setWindowIcon(QIcon("resources/logo.jpg"))
        f = open("resources/mainwindow.css", 'r')
        stylesheet = f.read()
        self.main_window.setStyleSheet(stylesheet)

        self.label.setPixmap(QPixmap("resources/logo.jpg"))
        self.pushButton.clicked.connect(self.openRT)
        self.pushButton_2.clicked.connect(self.openRP)

    def openRT(self):
        """  """
        real_time_dialog = DataRT(self.main_window)
        real_time_dialog.saveFileName()

    def openRP(self):
        """   """
        replay_dialog = Data(self.main_window)
        replay_dialog.openFileName()
