from PyQt4 import QtGui
from flight_dataUI import Ui_Dialog

class flightData(QtGui.QDialog,Ui_Dialog):
    def __init__(self,parent=None):
        QtGui.QDialog.__init__(self,parent)
        self.setupUi(self)

