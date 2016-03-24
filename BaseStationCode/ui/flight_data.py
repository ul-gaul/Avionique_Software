from PyQt4 import QtGui
from .flight_dataUI import Ui_Dialog
from .analyse import AnalyseRocketData

class flightData(QtGui.QDialog,Ui_Dialog):
    def __init__(self,parent=None):
        QtGui.QDialog.__init__(self,parent)
        self.setupUi(self)

    def init_widgets(selfself):
        self.analyseButton.clicked.connect(self.open_analyseWindow())

    def open_analyseWindow(self):
        rocketData = AnalyseRocketData(self)
        rocketData.exec_()


