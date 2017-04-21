from .dataUI import Ui_data
from PyQt5.QtWidgets import QWidget, QFileDialog, QMainWindow
from PyQt5 import QtCore, QtGui

class Data(QMainWindow, Ui_data):

    def __init__(self):
        super.__init__()
        self.initUI()

    def initUI(self):
        pass

    def openFileName(self):

        self.filename, _= QFileDialog.getOpenFileName(self, "Open File", "CSV Files (*.csv)")

    def saveFileName(self):

        self.filename, _ = QFileDialog.getSaveFileName(self, "Save File", d.now().strftime("%Y-%m-%d_%Hh%Mm")+".csv",
                                                       "All Files (*);; CSV Files (*.csv)")
