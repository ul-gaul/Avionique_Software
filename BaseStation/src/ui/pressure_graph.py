from PyQt5 import QtWidgets, QtCore
from pyqtgraph import PlotWidget, mkPen, mkBrush, TextItem
from src.ui.utils import set_minimum_expanding_size_policy


class PressureGraph(PlotWidget):

    def __init__(self, parent: QtWidgets.QWidget):
        super().__init__(parent)

        self.set_graph_title("Pressure")
        self.set_graph_bottom_legend("Temps (s)")
        self.set_graph_left_legend("Pressure (p)")

        self.pressure_curve = self.plot([0], [0], pen=mkPen(color='k', width=3))

        self.current_timestamp = 0
        self.current_pressure = 0
        self.current_pressure_text = TextItem("", anchor=(1, 1), color=(0, 0, 0, 0))
        self.current_pressure_point = self.plotItem.scatterPlot([], [], pxMode=True, size=8, brush=mkBrush(color='r'))
        self.addItem(self.current_pressure_text, ignoreBounds=True)

    def draw_pressure_curve(self, timestamps: list, pressures: list):
        nb_points = len(pressures)

        if nb_points > 0:
            self.current_timestamp = timestamps[-1]
            self.current_pressure = int(pressures[-1])

            self.altitude_curve.setData(timestamps, pressures)
            self.current_altitude_point.setData([self.current_timestamp], [self.current_altitude])
            self.current_altitude_text.setPos(self.current_timestamp, self.current_altitude)
            self.current_altitude_text.setColor(color='k')

            self.current_pressure_text.setText("{}p".format(self.current_pressure))

    def set_graph_title(self, title: str):
        self.plotItem.setTitle(title)

    def set_graph_bottom_legend(self, name: str):
        self.plotItem.setLabel("bottom", name)

    def set_graph_left_legend(self, name: str):
        self.plotItem.setLabel("left", name)

    def reset_altitude(self):
        self.pressure_curve.clear()
        self.current_timestamp = 0
        self.current_pressure = 0
        self.current_pressure_point.clear()
        self.current_pressure_point.setPos(0, self.current_altitude)
        self.current_pressure_text.setColor(color=(0, 0, 0, 0))

    def reset(self):
        self.reset_altitude()
