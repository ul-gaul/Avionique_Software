from PyQt4 import QtGui
from .analysisUI import Ui_Dialog

class analysisData(QtGui.QDialog, Ui_Dialog):
    def __init__(self,Parent=None):
        QtGui.QDialog.__init__(self,Parent)
        self.setupUi(self)

    def init_widgets(self):

        self.returnPush.clicked.connect(self.Retour)

    def ReturnMainWindow(self):

        Retour = MainWindow(self)
        Retour.exec()
