from PyQt4 import QtGui
from .flight_dataUI import Ui_Dialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import random


class FlightData(QtGui.QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)


        self.figure = plt.figure() # FlightData.figure = matplotlib.pyplot.figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas1 = FigureCanvas(self.figure)
        self.canvas2 = FigureCanvas(self.figure)
        self.canvas3 = FigureCanvas(self.figure)
        ax = self.figure.add_subplot(111)
        ax.hold(False)

        self.speedLayout.addWidget(self.canvas) # Créé un widget et met le canvas


        self.heightLayout.addWidget(self.canvas1)

        self.mapLayout.addWidget(self.canvas2)

        self.angleLayout.addWidget(self.canvas3)

        self.init_widgets()


    def init_widgets(self):
        self.analyseButton.clicked.connect(self.open_analysedata)
        #self.plotte()

    def open_analysedata(self):
        self.done(2)  # Ferme et delete la fenêtre Dialog et retourne 2 comme valeur à results dans main_window.py

    def plotte(self):
        data = [random.random() for i in range(10)]
        s = sum(data)
        avg = round(s/len(data), 4)
        print(avg)

        ax.plot(data, '*-')
"""
        data1 = [random.random() for i in range(10)]
        c = sum(data1)
        print(c)
        ax1 = self.figure.add_subplot(122)
        ax1.hold(False)
        ax1.plot(data1, '*-')
"""