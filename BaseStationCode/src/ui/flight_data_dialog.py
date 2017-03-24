import random
from queue import Queue, Empty
from PyQt5 import QtGui, QtCore
from rocket_data.csv_data_writer import CsvDataWriter
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from src.csv_data_writer import CsvDataWriter
from src.serial_reader import SerialReader
from .data_processing import DataProcessing
#from communication.serial_reader import AcquisitionThread

class DataHandlingThread(QtCore.QThread):
    data_received = QtCore.pyqtSignal()

    def __init__(self, acquisition_queue, data_processing):
        QtCore.QThread.__init__(self)
        self.acquisition_queue = acquisition_queue
        self.data_proc = data_processing
        self.exit_flag = True

    def run(self):
        self.exit_flag = False
        csv_writer = CsvDataWriter()
        while not self.exit_flag:
            try :
                rocket_data = self.acquisition_queue.get(block=False, timeout=2)
                # rocket_data.print_data()
                csv_writer.write_line(rocket_data)
                self.data_proc.add_data(rocket_data)
                self.data_received.emit()
            except Empty:
                pass

    def stop(self):
        self.exit_flag = True


class FlightDataDialog(QtGui, Ui_Dialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)

        self.data_proc = DataProcessing()
        queue = Queue(maxsize=100000)
        self.acquisition_thread = SerialReader(queue)
        self.data_handling_thread = DataHandlingThread(queue, self.data_proc)

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

        """Create the canvas widget in the UI"""
        self.speedLayout.addWidget(self.canvas['speed'])  # Creates the canvas for speed
        self.heightLayout.addWidget(self.canvas['height'])  # Creates the canvas for height
        self.mapLayout.addWidget(self.canvas['map'])  # Creates the canvas for map
        self.angleLayout.addWidget(self.canvas['angle'])  # Creates the canvas for angle

        self.init_widgets()  # Once the Dialog exist, automatically initiate self.

        self.Atimer = 0

    def init_widgets(self):
        """Connect the buttons to their respective method"""
        # self.analyseButton.clicked.connect(self.open_analysedata)
        self.analyseButton.setEnabled(False)
        self.stopButton.clicked.connect(self.stop_plotting)
        self.stopButton.setEnabled(False)
        self.startButton.clicked.connect(self.start_plotting)
        self.exitPush.clicked.connect(self.exit_UI)
        self.data_handling_thread.data_received.connect(self.draw_plots_LCD)

        self.heightLCD.setNumDigits(7)
        self.speedLCD.setNumDigits(7)

    def exit_UI(self):
        self.done(3)

    def open_analysedata(self):
        """Closes and deletes Dialog Window and return the integer 2
        to main_window.py which will connect to and open analysis.py"""
        self.done(2)

    def stop_plotting(self):
        """Ends the plotting and the thread"""
        self.startButton.setEnabled(True)
        self.stopButton.setEnabled(False)
        self.data_handling_thread.stop()
        self.acquisition_thread.stop()

    def start_plotting(self):
        """Starts the thread and the drawing of each plot,
        calls the method fetch_data/generate_random_listevery 1 second"""
        # TODO : Reset plots before plotting
        self.startButton.setEnabled(False)
        self.stopButton.setEnabled(True)
        self.acquisition_thread.start()
        self.data_handling_thread.start()

    def draw_plots_LCD(self):
        """Clear graphs"""
        # TODO : uncomment this section and optimize speed (for now, if acquisition sampling frequency is over 0.2 Hz, it doesn't work because it's too slow)
        # self.axs["height"].clear()
        # self.axs["speed"].clear()
        # self.axs["map"].clear()
        # self.axs["angle"].clear()
        # """Draw updated data in graphs and LCD widgets"""
        # self.draw_plot("height", self.data_proc.split_data["alt"])
        # self.draw_plot("speed", self.data_proc.split_data["verticalSpeed"])
        # self.draw_plot("angle", self.data_proc.split_data["temp1"])
        # self.draw_plot("angle", self.data_proc.split_data["temp2"])
        # self.draw_plot("map", self.data_proc.split_data["accx"])
        self.showlcd(self.data_proc.split_data["verticalSpeed"], self.data_proc.split_data["alt"], self.data_proc.split_data["meanlat"], self.data_proc.split_data["meanlong"])


    def draw_plot(self, target,data):
        """Call plot function and draw on the target key in self.axs and self.canvas,
        with the desired data, usually a list"""
        self.axs[target].plot(self.data_proc.split_data["time"], data, '--')
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

    def showlcd(self, sp, alt, lat, long):
        if sp != []:
            speed = round(sp[-1], 2)
        else:
            speed = None

        if alt != []:
            height = round(alt[-1], 2)
        else:
            height = None

        if lat != []:
            lattitude = lat[-1]
        else:
            lattitude = None

        if long != []:
            longitude = long[-1]
        else:
            longitude = None

        coords_lat = str(lattitude)
        coords_long = str(longitude)
        speed_text = str(speed)
        height_text = str(height)

        self.LatLCD.display(coords_lat)
        self.longLCD.display(coords_long)
        self.heightLCD.display(height_text)
        self.speedLCD.display(speed_text)
