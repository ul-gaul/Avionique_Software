from datetime import datetime as d
from PyQt5.QtWidgets import QWidget, QFileDialog
from PyQt5 import QtCore, QtGui

from .dataUI import Ui_Data


class Data(Ui_Data):

    def __init__(self, main_window):
        self.filename = ""
        self.setupUi(main_window)
        self.initUI()

    def initUI(self):
        self.label.setPixmap(QtGui.QPixmap("resources/logo.jpg"))

    def openFileName(self):

        self.filename, _ = QFileDialog.getOpenFileName(caption="Open File", filter="CSV Files (*.csv)")

    def saveFileName(self):

        self.filename, _ = QFileDialog.getSaveFileName(caption="Save File",
                                                       directory=d.now().strftime("%Y-%m-%d_%Hh%Mm")+".csv",
                                                       filter="All Files (*);; CSV Files (*.csv)")
