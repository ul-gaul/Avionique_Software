from PyQt4 import QtGui
from .analysisUI import Ui_Dialog

class analysisData(QtGui.QDialog, Ui_Dialog):
    def __init__(self,Parent=None):
        QtGui.QDialog.__init__(self,Parent)
        self.setupUi(self)
        self.init_widgets()

    def init_widgets(self):

        self.returnPush.clicked.connect(self.ReturnMainWindow)
        self.closePush.clicked.connect(self.CloseProgramm)

    def ReturnMainWindow(self):

        self.close()

    def CloseProgramm(self):
        self.done(11)
