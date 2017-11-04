from PyQt5 import QtWidgets, QtCore, QtGui
from src.ui.utils import set_minimum_expanding_size_policy


class Thermometer(QtWidgets.QWidget):

    def __init__(self, parent: QtWidgets.QWidget):
        super().__init__(parent)

        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("thermometer_gridLayout")

        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self._create_graduation_labels()
        self.gridLayout.addLayout(self.verticalLayout_7, 1, 1, 1, 1)

        self.label_20 = QtWidgets.QLabel(self)
        self.label_20.setObjectName("label_20")
        self.label_20.setText("°C")
        self.gridLayout.addWidget(self.label_20, 0, 1, 1, 1)

        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_14.addItem(spacerItem9)
        self.label_8 = QtWidgets.QLabel(self)
        self.label_8.setObjectName("label_8")
        self.label_8.setText("Température")
        self.horizontalLayout_14.addWidget(self.label_8)
        spacerItem15 = QtWidgets.QSpacerItem(30, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_14.addItem(spacerItem15)
        self.gridLayout.addLayout(self.horizontalLayout_14, 0, 0, 1, 1)

        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        spacerItem10 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.MinimumExpanding,
                                             QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem10)

        color_gradient = self._create_color_gradient()
        self.horizontalLayout_13.addWidget(color_gradient)

        vertical_slider = self._create_vertical_slider()
        self.horizontalLayout_13.addWidget(vertical_slider)

        self.gridLayout.addLayout(self.horizontalLayout_13, 1, 0, 1, 1)
        spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem11, 0, 2, 1, 1)
        spacerItem12 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.MinimumExpanding,
                                             QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem12, 1, 2, 1, 1)

    def _create_graduation_labels(self):
        for i in range(11):
            label = self._create_graduation_label(str(100 - 10 * i))
            self.verticalLayout_7.addWidget(label)

    def _create_graduation_label(self, temperature_graduation: str):
        label = QtWidgets.QLabel(self)
        label.setObjectName("thermometer_label_" + temperature_graduation)
        label.setText(temperature_graduation)
        return label

    def _create_color_gradient(self):
        color_gradient = QtWidgets.QLabel(self)
        set_minimum_expanding_size_policy(color_gradient)
        color_gradient.setMinimumSize(QtCore.QSize(50, 273))
        color_gradient.setMaximumSize(QtCore.QSize(100, 400))
        color_gradient.setText("")
        color_gradient.setObjectName("thermometer_color_gradient")
        color_gradient.setPixmap(QtGui.QPixmap("resources/gradient.png"))
        return color_gradient

    def _create_vertical_slider(self):
        vertical_slider = QtWidgets.QSlider(self)
        vertical_slider.setEnabled(True)
        vertical_slider.setMaximum(100)
        vertical_slider.setTracking(False)
        vertical_slider.setOrientation(QtCore.Qt.Vertical)
        vertical_slider.setInvertedAppearance(False)
        vertical_slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        vertical_slider.setTickInterval(10)
        vertical_slider.setObjectName("thermometer_verticalSlider")
        return vertical_slider

    def get_layout(self):
        return self.gridLayout

    def set_temperature(self, temperature: float):
        if temperature < 0:
            value = 0
        elif temperature > 100:
            value = 100
        else:
            value = round(temperature)

        self.verticalSlider.setValue(value)
