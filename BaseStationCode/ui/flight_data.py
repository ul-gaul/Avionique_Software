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
#       Creates a figure widget self.name = FigureCanvas(self.figure)
        self.speedGraph = FigureCanvas(self.figure)
        self.heightGraph = FigureCanvas(self.figure)
        self.mapGraph = FigureCanvas(self.figure)
        self.angleGraph = FigureCanvas(self.figure)
# -------------------------------------------------------------
        self.speedLayout.addWidget(self.speedGraph)  # insert widget "speedGraph" in speedLayout
        self.heightLayout.addWidget(self.heightGraph)  # insert widget "heightGraph" in heightLayout
        self.mapLayout.addWidget(self.mapGraph)  # insert widget "mapGraph" in mapLayout
        self.angleLayout.addWidget(self.angleGraph)  # insert widget "angleGraph" in angleLayout
        self.ax = self.figure.add_subplot(111)
        self.ax.hold(False)
        self.init_widgets()

    def init_widgets(self):
        self.analyseButton.clicked.connect(self.open_analysedata)
        self.draw_plot()

    def open_analysedata(self):
        self.done(2)  # Ferme et delete la fenêtre Dialog et retourne 2 comme valeur à results dans main_window.py

    def draw_plot(self):
        data = [random.random() for i in range(10)]
        s = sum(data)
        avg = round(s/len(data), 4)
        print(avg)
#        ax = self.figure.add_subplot(111)
#        ax.hold(False)
        self.ax.plot(data, '-*')
"""
        data1 = [random.random() for i in range(10)]
        c = sum(data1)
        print(c)
        ax1 = self.figure.add_subplot(122)
        ax1.hold(False)
        ax1.plot(data1, '*-')
"""