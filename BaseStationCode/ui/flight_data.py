from PyQt4 import QtGui
from .flight_dataUI import Ui_Dialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import random


class FlightData(QtGui.QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.figs = {}
        self.canvas = {}
        self.axs = {}
        plot_names = ['speed', 'height', 'map', 'angle']
        for pn in plot_names:
            fig = Figure()
            self.canvas[pn] = FigureCanvas(fig)
            ax = fig.add_subplot(1, 1, 1)

            self.figs[pn] = fig
            self.axs[pn] = ax

        self.speedLayout.addWidget(self.canvas['speed'])
        self.heightLayout.addWidget(self.canvas['height'])
        self.mapLayout.addWidget(self.canvas['map'])
        self.angleLayout.addWidget(self.canvas['angle'])
        data = [random.random() for i in range(10)]
#        s = sum(data)
#        avg = round(s/len(data), 4)
#        print(avg)
#        ax = self.figure.add_subplot(111)
#        ax.hold(False)
        self.draw_plot('speed', data)
    def init_widgets(self):
        self.analyseButton.clicked.connect(self.open_analysedata)
        #self.draw_plot()

    def open_analysedata(self):
        self.done(2)  # Ferme et delete la fenêtre Dialog et retourne 2 comme valeur à results dans main_window.py

    def draw_plot(self, target, data):
        self.axs[target].plot(data, '-*')
        self.canvas[target].draw_idle()


"""        self.figure = plt.figure() # FlightData.figure = matplotlib.pyplot.figure()
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
        self.init_widgets()"""
