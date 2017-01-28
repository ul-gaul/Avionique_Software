from PyQt4 import QtGui
from .analysisUI import Ui_Dialog
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class analysisData(QtGui.QDialog, Ui_Dialog):
    def __init__(self,Parent=None):
        QtGui.QDialog.__init__(self,Parent)
        self.setupUi(self)
        self.figs = {}
        self.canvas = {}
        self.axs = {}
        plot_names = ["height", "stress", "speed", "acceleration", "temperature", "angle"]
        for pn in plot_names:
            fig = Figure()
            self.canvas[pn] = FigureCanvas(fig)
            ax = fig.add_subplot(1,1,1)

            self.figs[pn] = fig
            self.axs[pn] = ax
        self.postHeightLayout.addWidget(self.canvas["height"])
        self.stressLaout.addWidget(self.canvas["stress"])
        self.speedLayout.addWidget(self.canvas["speed"])
        self.accLayout.addWidget(self.canvas["acceleration"])
        self.postTemperatureLayout.addWidget(self.canvas["temperature"])
        self.angleLayout.addWidget(self.canvas["angle"])
        self.init_widgets()

    def init_widgets(self):

        self.returnPush.clicked.connect(self.ReturnMainWindow)
        self.closePush.clicked.connect(self.CloseProgramm)

    def ReturnMainWindow(self):

        self.close()

    def CloseProgramm(self):
        self.done(11)

    def draw_plot(self, target, data):
        self.axs[target].plot(data, '-*')
        self.canvas[target].draw_idle()
