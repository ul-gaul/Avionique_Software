from PyQt4 import QtGui
from .flight_dataUI import Ui_Dialog
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import random
import time
import matplotlib.animation as Animation
import numpy as np

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
        self.init_widgets()
        #self.ani = Animation.FuncAnimation(self.figs["speed"], self.generate_random_list, 1000)
        for pn in ['speed', 'height', 'map', 'angle']:
            self.ani = Animation.FuncAnimation(self.figs[pn], self.generate_random_list, 1000)
    def init_widgets(self):
        self.analyseButton.clicked.connect(self.open_analysedata)


    def open_analysedata(self):
        self.done(2)  # Closes and deletes Dialog Window and return the integer 2 to main_window.py which will
        #               connect to and open analysis.py

    def draw_plot(self, target, data):
        self.axs[target].plot(data, '-*')
        self.canvas[target].draw_idle()

    def generate_random_list(self, i):
        data_list = []
        data_list1 = []
        data_list2 = []
        data_list3 = []
        self.axs["height"].clear()
        self.axs["speed"].clear()
        self.axs["map"].clear()
        self.axs["angle"].clear()

        for j in range(i):
            data_list.append(random.randrange(0,100))

        for j in data_list:
            data_list1.append(j+random.randrange(-10,10))
            data_list2.append(j*random.randrange(0,5))
            data_list3.append(j/random.randrange(1,10))
        self.draw_plot("speed", data_list)
        self.draw_plot("height", data_list1)
        self.draw_plot("map", data_list2)
        self.draw_plot("angle", data_list3)


    def generate_cosinus(self, i):
        cos = np.cos
        yar = []
        yar1 = []
        yar2 = []
        yar3 = []
        for pn in ['speed', 'height', 'map', 'angle']:
            self.axs[pn].clear()

        for j in range(i):
            yar.append((cos((i*500/1000)*np.pi)))

        for obj in yar:
            yar1.append(obj/4)
            yar2.append(obj*20)
            yar3.append(obj/10)

        self.draw_plot("height", yar)
        self.draw_plot("speed", yar1)
        self.draw_plot("map", yar2)
        self.draw_plot("angle", yar3)

