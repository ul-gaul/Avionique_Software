from PyQt4 import QtGui, QtCore
from .analyseUI import Ui_QDialog

class AnalyseRocketData(QtGui.QDialog, Ui_QDialog):
    def __init__(self,parent=None):
        QtGui.QDialog.__init__(self,parent)
        self.setupUi(self)