from PyQt5 import QtWidgets, QtCore, QtGui
from pyqtgraph import PlotWidget, mkPen, mkBrush, TextItem
import pyqtgraph as pg

from src.ui.utils import set_minimum_expanding_size_policy


class AltitudeGraph(PlotWidget):

    def __init__(self, parent: QtWidgets.QWidget):
        super().__init__(parent)

        self.setMinimumSize(QtCore.QSize(400, 150))
        set_minimum_expanding_size_policy(self)
        self.setObjectName("altitudeGraph")

        self.plotItem.setTitle("Altitude")
        self.plotItem.setLabel("bottom", "Temps", "Sec")
        self.plotItem.setLabel("left", "Altitude (ft)")

        self.altitude_curve = self.plot([0], [0], pen=mkPen(color='k', width=3))

        self.current_altitude_text = None
        self.current_altitude_point = self.plotItem.scatterPlot([], [], pxMode=True, size=8, brush=mkBrush(color='r'))

        self.simulation_curve = None

    def draw(self, values: list):
        print('attemting to draw altitude graph.')
        nb_points = len(values)

        if nb_points > 0:
            current_altitude = int(values[-1])
            print('really drawing altitude graph.')
            self.altitude_curve.setData(values)
            QtGui.QApplication.processEvents()
            self.current_altitude_point.setData([nb_points - 1], [current_altitude])
            # FIXME: this makes the app crash randomly when resizing the axis of the graph
            # self.update_current_altitude_text(nb_points, current_altitude)

    def update_current_altitude_text(self, nb_points: int, current_altitude: int):
        if self.current_altitude_text is not None:
            self.removeItem(self.current_altitude_text)

        if nb_points >= 2:
            self.current_altitude_text = TextItem(text=str(current_altitude), color='r', anchor=(1, 1))
            self.current_altitude_text.setPos(nb_points - 1, current_altitude)
            self.addItem(self.current_altitude_text)

    def set_target_altitude(self, altitude):
        self.plotItem.addLine(y=altitude, pen=mkPen(color=(15, 236, 20), width=3, style=QtCore.Qt.DashDotLine))

    def show_simulation(self, time: list, altitude: list):
        if self.simulation_curve is None:
            self.simulation_curve = self.plot(time, altitude, pen=mkPen(color='b', width=3))
        else:
            self.simulation_curve.setData(time, altitude)
