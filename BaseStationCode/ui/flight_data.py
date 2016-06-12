from PyQt4 import QtGui, QtCore
from .flight_dataUI import Ui_Dialog
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import random
import time
import matplotlib.animation as Animation
import numpy as np
from .data_processing import DataProcessing
from ..communication.serialReader import SerialReader
from ..rocket_data import rocket_packet

class LoopThread(QtCore.QThread):
    def __init__(self, flightdata):
        QtCore.QThread.__init__(self)
        self.flightdata = flightdata
        self.signal = QtCore.SIGNAL("signal")
        self.exitFlag = False

    def run(self):
        while True:
            if self.exitFlag == True:
                break
            else:
                dataList = self.flightdata.serialReader.get()
                self.flightdata.data_proc.add_data(dataList)
                self.emit(self.signal,"Hi from Thread")
                time.sleep(1)

    def stop(self):
        """Thread is ended when called"""
        self.exitFlag = True


class FlightData(QtGui.QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)

        """Creates shortcut for signal emission to threads"""
        self.signal = QtCore.SIGNAL("signal")

        """Create DataProcessing"""
        self.data_proc = DataProcessing()

        """Create the serialReader"""
        self.serialReader = SerialReader("acquisition.csv")

        """Initialize figs, canvas and axs"""
        self.figs = {}  # Empty Dictionnary
        self.canvas = {}  # Empty Dictionnary
        self.axs = {}  # Empty Dictionnary

        """Add the keys speed, height, map and angle to figs"""
        plot_names = ['speed', 'height', 'map', 'angle']
        for pn in plot_names:
            fig = Figure()  # Give the variable fig the function Figure()
            self.canvas[pn] = FigureCanvas(fig)  # Creates the key pn and assiociates it with FigureCanvas
            ax = fig.add_subplot(1, 1, 1)  # Creates a plot

            self.figs[pn] = fig  # Each string of plot_names are a Figure()
            self.axs[pn] = ax  # Each string of plot_names are a plot defined by ax

        """Initiate the data_list for the method generate_random_list"""
        self.data_list = []
        self.data_list1 = []
        self.data_list2 = []
        self.data_list3 = []

        """Create the canvas widget in the UI"""
        self.speedLayout.addWidget(self.canvas['speed'])  # Creates the canvas for speed
        self.heightLayout.addWidget(self.canvas['height'])  # Creates the canvas for height
        self.mapLayout.addWidget(self.canvas['map'])  # Creates the canvas for map
        self.angleLayout.addWidget(self.canvas['angle'])  # Creates the canvas for angle

        self.init_widgets()  # Once the Dialog exist, automatically initiate self.

    def init_widgets(self):
        """Connect the buttons to their respective method"""
        self.analyseButton.clicked.connect(self.open_analysedata)
        self.stopButton.clicked.connect(self.stop_plotting)
        self.startButton.clicked.connect(self.start_plotting)
        #self.showlcd([10, 2, 14])


    def open_analysedata(self):
        """Closes and deletes Dialog Window and return the integer 2
        to main_window.py which will connect to and open analysis.py"""
        self.done(2)

    def stop_plotting(self):
        """Ends the plotting and the thread"""
        self.ani._stop()
        self.data_thread.stop()
        self.serialReader.exit()

    def start_plotting(self):
        """Starts the thread and the drawing of each plot,
        calls the method fetch_data/generate_random_listevery 1 second"""
        self.ani = Animation.FuncAnimation(self.figs["speed"], self.generate_random_list, interval= 100)
        self.serialReader.start()
        self.data_thread = LoopThread(self)
        self.connect(self.data_thread, self.data_thread.signal, self.draw_plots)
        self.data_thread.start()

    def draw_plots(self):
        """self.draw_plot("height", self.data_proc.data["alt"])
        self.draw_plot("speed", )
        self.draw_plot("angle", self.data_proc.data[])
        self.draw_plot("map", self.data_proc.data[])"""

        self.draw_plot("speed", self.data_list)
        self.draw_plot("height", self.data_list1)
        self.draw_plot("map", self.data_list2)
        self.draw_plot("angle", self.data_list3)

    def draw_plot(self, target, data):
        self.axs[target].plot(data, '-*')  # Will plot with one of the 4 plot_names and any given data in a list
        self.canvas[target].draw()

    def generate_random_list(self, i):
        self.axs["height"].clear()
        self.axs["speed"].clear()
        self.axs["map"].clear()
        self.axs["angle"].clear()

        self.data_list.append(random.randrange(0, 100))
        j = self.data_list[len(self.data_list)-1]
        self.data_list1.append(j+random.randrange(-10, 10))
        self.data_list2.append(j*random.randrange(0, 5))
        self.data_list3.append(j/random.randrange(1, 10))

    def fetch_data(self,i):
        self.axs["height"].clear()
        self.axs["speed"].clear()
        self.axs["map"].clear()
        self.axs["angle"].clear()
        self.data_proc.fetch_data()

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
        self.draw_plot("map", self.yar2)
        self.draw_plot("angle", yar3)

    def showlcd(self, data):
        speed = data[len(data)-1]
        text = str(speed)
        self.speedLCD.display(text)
