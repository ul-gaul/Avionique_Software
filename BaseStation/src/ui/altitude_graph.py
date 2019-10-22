from PyQt5 import QtWidgets, QtCore
from pyqtgraph import PlotWidget, mkPen, mkBrush, TextItem

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

        self.current_timestamp = 0
        self.current_altitude = 0
        self.current_altitude_text = TextItem("", anchor=(1, 1), color=(0, 0, 0, 0))
        self.current_altitude_point = self.plotItem.scatterPlot([], [], pxMode=True, size=8, brush=mkBrush(color='r'))
        self.addItem(self.current_altitude_text, ignoreBounds=True)

        self.simulation_curve = self.plot([], [], pen=mkPen(color='b', width=3))
        self.apogee = 0
        self.draw_apogee_plot = True
        self.apogee_text = TextItem("", anchor=(1, 1), color=(0, 0, 0, 0))
        self.apogee_point = self.plotItem.scatterPlot([], [], pxMode=True, size=9, brush=mkBrush(color='b'))
        self.addItem(self.apogee_text, ignoreBounds=True)

    def paintEvent(self, ev):
        self.apogee_text.setText("{}ft".format(int(self.apogee)))
        self.current_altitude_text.setText("{}ft".format(self.current_altitude))

        super(AltitudeGraph, self).paintEvent(ev)

    def draw_altitude_curve(self, timestamps: list, altitudes: list):
        nb_points = len(altitudes)

        if nb_points > 0:
            self.current_timestamp = timestamps[-1]
            self.current_altitude = int(altitudes[-1])

            self.altitude_curve.setData(timestamps, altitudes)
            self.current_altitude_point.setData([self.current_timestamp], [self.current_altitude])
            self.current_altitude_text.setPos(self.current_timestamp, self.current_altitude)
            self.current_altitude_text.setColor(color='k')

    def set_target_altitude(self, altitude):
        self.plotItem.addLine(y=altitude, pen=mkPen(color=(15, 236, 20), width=3, style=QtCore.Qt.DashDotLine))

    def show_simulation(self, time: list, altitude: list):
        self.simulation_curve.setData(time, altitude)

    def draw_apogee(self, values: list):
        if len(values) == 2:
            self.apogee = values[1]
            apogee_index = values[0]    # FIXME: use timestamps

            if self.draw_apogee_plot:
                self.apogee_text.setColor(color='b')
                self.draw_apogee_plot = False

            # self.apogee_point.setData([apogee_index], [self.apogee])
            # self.apogee_text.setPos(apogee_index, self.apogee)
        else:
            if not self.draw_apogee_plot:
                self.reset_apogee()

    def reset(self):
        self.reset_altitude()
        self.reset_apogee()
        self.reset_simulation()

    def reset_altitude(self):
        self.altitude_curve.clear()
        self.current_timestamp = 0
        self.current_altitude = 0
        self.current_altitude_point.clear()
        self.current_altitude_text.setPos(0, self.current_altitude)
        self.current_altitude_text.setColor(color=(0, 0, 0, 0))

    def reset_apogee(self):
        self.apogee = 0
        self.apogee_point.clear()
        self.apogee_text.setColor(color=(0, 0, 0, 0))
        self.draw_apogee_plot = True

    def reset_simulation(self):
        self.simulation_curve.clear()
