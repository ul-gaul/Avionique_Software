from PyQt5 import QtWidgets, QtCore
from pyqtgraph import PlotWidget, mkPen, TextItem, mkBrush

from src.ui.utils import set_minimum_expanding_size_policy


class Map(PlotWidget):
    def __init__(self, parent: QtWidgets.QWidget):
        super().__init__(parent)

        self.setMinimumSize(QtCore.QSize(400, 150))
        set_minimum_expanding_size_policy(self)
        self.setObjectName("map")

        self.plotItem.setTitle("Position relative au camp")
        self.plotItem.setLabel("bottom", "Est", "m")
        self.plotItem.setLabel("left", "Nord", "m")
        self.plotItem.showGrid(x=True, y=True)

        self.positions_on_map = self.plot([0], [0], pen=mkPen(color='k', width=3))

        self.current_coordinates = 0, 0
        self.current_coordinates_text = TextItem("", anchor=(1, 1), color=(0, 0, 0, 0))
        self.current_coordinates_text.setText("lat: {}\nlong: {}".format(0, 0))
        self.current_coordinates_point = self.plotItem.scatterPlot([], [], pxMode=True, size=8,
                                                                   brush=mkBrush(color='r'))
        self.addItem(self.current_coordinates_text, ignoreBounds=True)

    def draw_map(self, eastings: list, northings: list):
        if len(eastings) > 0:
            self.positions_on_map.setData(eastings, northings)

            self.current_coordinates_point.setData([eastings[-1:]], northings[-1:])
            self.current_coordinates_text.setPos(eastings[-1], northings[-1])
            self.current_coordinates_text.setColor(color='k')

    def reset(self):
        self.positions_on_map.clear()

        self.current_coordinates = 0, 0
        self.current_coordinates_point.clear()
        self.current_coordinates_text.setPos(0, 0)
        self.current_coordinates_text.setColor(color=(0, 0, 0, 0))
