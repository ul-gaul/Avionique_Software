from PyQt4 import QtCore, QtGui
from flight_dataUI import Ui_Dialog

class flightData(QtGui,QtCore,Ui_Dialog):
    def __init__(self,parent=None):
        QtGui.QDialog.__init__(self,parent)
        self.setupUi(self)

