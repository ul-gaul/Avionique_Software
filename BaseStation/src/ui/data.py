from datetime import datetime as d
from PyQt5.QtWidgets import QFileDialog, QSlider
from PyQt5 import QtCore, QtGui

from src.ui.dataUI import Ui_Data
from src.ui.ExtendedQSlider import ExtendedQSlider


class Data(Ui_Data):

    def __init__(self, main_window):
        self.main_window = main_window
        self.horizontalSlider = None
        self.filename = ""
        self.setupUi(self.main_window)
        self.initUI()

    def initUI(self):
        f = open("resources/data.css", 'r')
        stylesheet = f.read()
        self.main_window.setStyleSheet(stylesheet)
        self.setup_slider()
        self.label.setPixmap(QtGui.QPixmap("resources/logo.jpg"))

        self.main_window.setWindowIcon(QtGui.QIcon("resource/logo.jpg"))

    def setup_slider(self):
        self.horizontalSlider = ExtendedQSlider(self.centralwidget)
        self.horizontalSlider.setEnabled(True)
        self.horizontalSlider.setMaximum(100)
        self.horizontalSlider.setPageStep(1)
        self.horizontalSlider.setSliderPosition(0)
        self.horizontalSlider.setTracking(True)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setTickPosition(QSlider.NoTicks)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.verticalLayout_5.addWidget(self.horizontalSlider)

    def openFileName(self):

        self.filename, _ = QFileDialog.getOpenFileName(caption="Open File", filter="CSV Files (*.csv)")

    def saveFileName(self):

        self.filename, _ = QFileDialog.getSaveFileName(caption="Save File",
                                                       directory=d.now().strftime("%Y-%m-%d_%Hh%Mm")+".csv",
                                                       filter="All Files (*);; CSV Files (*.csv)")
