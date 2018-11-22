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

        self.current_altitude = 0
        self.current_altitude_text = TextItem("", color='k')
        self.current_altitude_point = self.plotItem.scatterPlot([], [], pxMode=True, size=8, brush=mkBrush(color='r'))
        self.addItem(self.current_altitude_text)

        self.simulation_curve = None

        self.apogee = None
        self.apogee_text = TextItem("", anchor=(0.5, 1), color='b')
        self.apogee_point = self.plotItem.scatterPlot([], [], pxMode=True, size=8, brush=mkBrush(color='b'))
        self.addItem(self.apogee_text)

        self.apogee_dict = []

    def paintEvent(self, ev):
        self.apogee_text.setText("{}ft".format(self.apogee))
        self.current_altitude_text.setText("{}ft".format(self.current_altitude))

        super(AltitudeGraph, self).paintEvent(ev)

    def set_apogee(self, values: list):
        min_altitude = 0
        index = 0

        for i in range(len(values) - 1):
            if min_altitude < values[i]:
                min_altitude = values[i]
                index = i

        self.apogee = min_altitude
        self.apogee_point.setData([index], [self.apogee])
        self.apogee_text.setPos(index, self.apogee)

    def draw(self, values: list): # Faire attention quand on reverse, il faut changer l apogee
        nb_points = len(values)

        if nb_points > 0:
            if self.apogee is None:
                self.apogee = max(values)
                self.apogee_dict.append(self.apogee)
                altitude_index = values.index(self.apogee)
                self.apogee_point.setData([altitude_index], [self.apogee])
                self.apogee_text.setPos(altitude_index, self.apogee)
            elif nb_points == 1:
                self.apogee_dict.clear()
                self.apogee_dict.append(values[0])

                self.apogee = values[0]
                self.apogee_point.setData([], [])
                self.apogee_text.setPos(0, self.apogee)

            self.current_altitude = int(values[-1])

            self.altitude_curve.setData(values)
            self.current_altitude_point.setData([nb_points - 1], [self.current_altitude])
            self.current_altitude_text.setPos(nb_points - 1, self.current_altitude)

            # self.set_apogee(values) #Beaucoup plus lent.
            # Fix: Faire une liste de tout les apogee possible, le mettre dans un dic, et remove si trop loin.

            # if self.current_altitude > self.apogee:
            #     self.apogee = self.current_altitude
            #     self.apogee_point.setData([nb_points - 1], [self.current_altitude])
            #     self.apogee_text.setPos(nb_points - 1, self.current_altitude)


            #if len(self.apogee_dict) > 1 and self.apogee_dict.index(self.apogee_dict[-1]) < nb_points:

            if self.current_altitude > self.apogee_dict[-1]:
                self.apogee_dict.append(values[nb_points-1])
                self.apogee = self.current_altitude
                self.apogee_point.setData([nb_points - 1], [self.current_altitude])
                self.apogee_text.setPos(nb_points - 1, self.current_altitude)

            print(self.values.index(self.apogee_dict[-1]), nb_points)
            rg_index = None
            for i in range(len(values)):
                if values[i] == self.apogee_dict[-1]:
                    rg_index = i
                    break
            if rg_index > nb_points:
                self.apogee_dict.pop()

            # Il faut donc recuperer l index de la derniere apogee dans values.
            # if len(self.apogee_dict) > 1 and self.values.index(self.apogee_dict[-1]) > nb_points:
            #     self.apogee_dict.pop()

    def set_target_altitude(self, altitude):
        self.plotItem.addLine(y=altitude, pen=mkPen(color=(15, 236, 20), width=3, style=QtCore.Qt.DashDotLine))

    def show_simulation(self, time: list, altitude: list):
        if self.simulation_curve is None:
            self.simulation_curve = self.plot(time, altitude, pen=mkPen(color='b', width=3))
        else:
            self.simulation_curve.setData(time, altitude)
