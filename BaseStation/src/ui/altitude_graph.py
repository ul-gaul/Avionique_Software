from PyQt5 import QtWidgets, QtCore
from pyqtgraph import PlotWidget, mkPen, mkBrush, TextItem

from src.ui.utils import set_minimum_expanding_size_policy


class ApogeeCalculator:

    def __init__(self):
        self.points = None
        self.potential_apogee = {}

    def init(self, entire_values: list):
        self.potential_apogee.clear()
        self.points = entire_values

    def update(self, values: list):
        self.points = values

    def set_potential_apogee(self):
        for i in range(len(self.points) - 1):
            if self.apogee < self.points[i]:
                self.potential_apogee[i] = self.points[i]

    def get_apogee(self, current_point):
        new_apogee = 0

        if self.points[current_point] in self.potential_apogee:
            new_apogee = self.points[current_point]
        else:
            for key, value in self.potential_apogee.items():
                if new_apogee < value:
                    new_apogee = value
                    if key == current_point:
                        break

        return new_apogee


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

        self.current_altitude = 0
        self.current_altitude_text = TextItem("", color='k')
        self.current_altitude_point = self.plotItem.scatterPlot([], [], pxMode=True, size=8, brush=mkBrush(color='r'))
        self.addItem(self.current_altitude_text)

        self.simulation_curve = None

        self.apogee = None
        self.apogee_text = TextItem("", anchor=(0.5, 1), color='b')
        self.apogee_point = self.plotItem.scatterPlot([], [], pxMode=True, size=8, brush=mkBrush(color='b'))
        self.addItem(self.apogee_text)

        self.potential_apogee = {}

    def paintEvent(self, ev):
        self.apogee_text.setText("{}ft".format(int(self.apogee)))
        self.current_altitude_text.setText("{}ft".format(self.current_altitude))

        super(AltitudeGraph, self).paintEvent(ev)

    def draw(self, values: list):
        nb_points = len(values)

        if nb_points > 0:
            if self.apogee is None:
                #init ApogeeCalculator
                pass
            elif nb_points == 1:
                self.apogee = 0

            self.current_altitude = int(values[-1])

            self.altitude_curve.setData(values)
            self.current_altitude_point.setData([nb_points - 1], [self.current_altitude])
            self.current_altitude_text.setPos(nb_points - 1, self.current_altitude)

            self.set_apogee(values, nb_points-1)

    def set_target_altitude(self, altitude):
        self.plotItem.addLine(y=altitude, pen=mkPen(color=(15, 236, 20), width=3, style=QtCore.Qt.DashDotLine))

    def show_simulation(self, time: list, altitude: list):
        if self.simulation_curve is None:
            self.simulation_curve = self.plot(time, altitude, pen=mkPen(color='b', width=3))
        else:
            self.simulation_curve.setData(time, altitude)
