from PyQt5 import QtWidgets
from src.ui.pressure_graph import PressureGraph


class DataMotorWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.pressure_graph = PressureGraph(self)

    def draw_pressure(self, timestamps: list, pressures: list):
        self.pressure_graph.draw_altitude_curve(timestamps, pressures)

    def reset(self):
        self.pressure_graph.reset()
