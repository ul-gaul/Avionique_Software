from .main_windowUI import Ui_MainWindow
from PyQt4 import QtGui
from .flight_data import flightData
from .analysis import analysisData

class MainWindow(QtGui.QMainWindow,Ui_MainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self,parent)
        self.setupUi(parent)
        self.init_widgets()

    def init_widgets(self):
        self.flightDataPush.clicked.connect(self.open_flightData)
        #self.analysisPush.clicked.connect(self.open_analyseDialog())

    def open_flightData(self):
        flight_data = flightData(self)
        flight_data.exec_()

    #def open_analyseDialog(self):
       # postData = analysisData(self)
        #postData.exec_()



