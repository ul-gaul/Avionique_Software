from PyQt4 import QtGui
from .flight_dataUI import Ui_Dialog
from .analysis import analysisData

class flightData(QtGui.QDialog,Ui_Dialog):
    def __init__(self,parent=None):
        QtGui.QDialog.__init__(self,parent)
        self.setupUi(self)

    def init_widgets(self):
        self.analyseButton.clicked.connect(self.open_analyseData)

    def open_analyseData(self):

        postData = analysisData(self)
        postData.exec_()


