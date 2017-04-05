from .mainwindowUI import Ui_MainWindow
from PyQt5.QtWidgets import QFileDialog, QApplication
from PyQt5 import QtCore, QtGui
from datetime import datetime as d


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.pushButton.clicked.connect(self.saveFileName)
        self.pushButton_2.clicked.connect(self.openFileName)

    def openFileName(self):

        self.filename, _= QFileDialog.getOpenFileName(self, "Open File", "CSV Files (*.csv)")

    def saveFileName(self):

        self.filename, _ = QFileDialog.getSaveFileName(self, "Save File", d.now().strftime("%Y-%m-%d_%Hh%Mm")+".csv",
                                                       "All Files (*);; CSV Files (*.csv)")



