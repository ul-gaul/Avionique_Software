from PyQt4 import QtGui
from .flight_dataUI import Ui_Dialog
from .analysis import analysisData

class flightData(QtGui.QDialog,Ui_Dialog):
    def __init__(self,parent=None):
        QtGui.QDialog.__init__(self,parent)
        self.setupUi(self)
        self.init_widgets()

    def init_widgets(self):
        self.analyseButton.clicked.connect(self.open_analyseData)


    def open_analyseData(self):
        self.done(2) # Ferme et delete la fenêtre Dialog et retourne 2 comme valeur à results dans main_window.py




