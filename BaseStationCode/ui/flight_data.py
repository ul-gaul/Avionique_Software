from PyQt4 import QtGui
from .flight_dataUI import Ui_Dialog
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
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

    def init_widgets(self):
        self.analyseButton.clicked.connect(self.open_analysedata)


    def open_analysedata(self):
        self.done(2)  # Closes and deletes Dialog Window and return the interger 2 to main_window.py which will
        #               connect to and open analysis.py

    def draw_plot(self, target, data):
        self.axs[target].plot(data, '-*')
        self.canvas[target].draw_idle()

