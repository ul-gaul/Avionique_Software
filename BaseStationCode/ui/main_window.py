from .main_windowUI import Ui_MainWindow
from PyQt4 import QtGui
from .flight_data import FlightData
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

    def open_flightData(self):
        flight_data = FlightData(self)
        #ani = Animation.FuncAnimation(flight_data.figs["speed"], flight_data.generate_random_list, 500)
        result = flight_data.exec_()
        if result == 2: #Si result = 2, ouvre le dialog d'analyse
            self.open_analyseDialog()

    def open_analyseDialog(self):
        postData = analysisData(self)
        results = postData.exec_()
        if results == 11:
            sys.exit()







