from .mainwindowUI import Ui_MainWindow
from PyQt5.QtWidgets import QFileDialog
from datetime import datetime as d


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        pass

    def openFileName(self):

        self.filename, _= QFileDialog.getOpenFileName()

    def saveFileName(self):

        self.filename, _ = QFileDialog.getSaveFileName(self, "Save File", d.now().strftime())



