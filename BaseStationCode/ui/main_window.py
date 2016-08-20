from .main_windowUI import Ui_MainWindow
from PyQt4 import QtGui
from .flight_data_dialog import FlightDataDialog
from .analysis import analysisData
import sys
import matplotlib.animation as Animation

class MainWindow(QtGui.QMainWindow,Ui_MainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self,parent)
        self.setupUi(parent)
        self.init_widgets()

    def init_widgets(self):
        self.flightDataPush.clicked.connect(self.open_flightData)
        self.analysisPush.clicked.connect(self.open_analyseDialog)
        self.analysisPush.setEnabled(False)

    def open_flightData(self):
        flight_data_dialog = FlightDataDialog(self)
        flight_data_dialog

        result = flight_data_dialog.exec_()
        if result == 2:  # Si result = 2, ouvre le dialog d'analyse
            self.open_analyseDialog()
        elif result == 3:
            sys.exit()

    def open_analyseDialog(self):
        postData = analysisData(self)
        results = postData.exec_()
        if results == 11:
            sys.exit()








